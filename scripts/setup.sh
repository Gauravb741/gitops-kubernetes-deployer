#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  setup.sh — One-shot environment bootstrap
#  Creates a Kind cluster, installs Argo CD, and deploys the GitOps demo.
# ══════════════════════════════════════════════════════════════════════════════
set -euo pipefail

# ── Colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'; BOLD='\033[1m'

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
header()  { echo -e "\n${BOLD}${CYAN}══ $* ══${NC}\n"; }

# ── Configuration ─────────────────────────────────────────────────────────────
CLUSTER_NAME="${CLUSTER_NAME:-gitops-demo}"
NAMESPACE="${NAMESPACE:-gitops-demo}"
ARGOCD_NAMESPACE="argocd"
ARGOCD_VERSION="${ARGOCD_VERSION:-stable}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ── 1. Prerequisites check ────────────────────────────────────────────────────
header "Checking Prerequisites"

check_tool() {
  if command -v "$1" &>/dev/null; then
    success "$1 found: $(command -v "$1")"
  else
    error "$1 is not installed. Please install it and re-run."
    exit 1
  fi
}

check_tool kubectl
check_tool kind
check_tool kustomize || {
  warn "kustomize not found — attempting to install..."
  curl -sSL https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh | bash
  sudo mv kustomize /usr/local/bin/ 2>/dev/null || mv kustomize "${HOME}/.local/bin/" 2>/dev/null || true
}
check_tool docker

# ── 2. Kind cluster ───────────────────────────────────────────────────────────
header "Kubernetes Cluster"

if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  success "Kind cluster '${CLUSTER_NAME}' already exists — skipping creation."
else
  info "Creating Kind cluster '${CLUSTER_NAME}'..."

  cat <<EOF | kind create cluster --name "${CLUSTER_NAME}" --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: ${CLUSTER_NAME}
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 8080
        protocol: TCP
      - containerPort: 443
        hostPort: 8443
        protocol: TCP
      - containerPort: 30080
        hostPort: 30080
        protocol: TCP
EOF
  success "Kind cluster '${CLUSTER_NAME}' created."
fi

# Set kubectl context
kubectl cluster-info --context "kind-${CLUSTER_NAME}" >/dev/null
success "kubectl connected to cluster 'kind-${CLUSTER_NAME}'."

# ── 3. Namespace ──────────────────────────────────────────────────────────────
header "Namespace"

if kubectl get namespace "${NAMESPACE}" &>/dev/null; then
  success "Namespace '${NAMESPACE}' already exists."
else
  kubectl create namespace "${NAMESPACE}"
  success "Namespace '${NAMESPACE}' created."
fi

# ── 4. Argo CD ────────────────────────────────────────────────────────────────
header "Argo CD Installation"

if kubectl get namespace "${ARGOCD_NAMESPACE}" &>/dev/null; then
  success "Argo CD namespace already exists."
else
  info "Creating Argo CD namespace..."
  kubectl create namespace "${ARGOCD_NAMESPACE}"
fi

if kubectl get deployment argocd-server -n "${ARGOCD_NAMESPACE}" &>/dev/null; then
  success "Argo CD already installed."
else
  info "Installing Argo CD (${ARGOCD_VERSION})..."
  kubectl apply -n "${ARGOCD_NAMESPACE}" \
    -f "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml"
  success "Argo CD manifests applied."
fi

# ── 5. Wait for Argo CD ───────────────────────────────────────────────────────
header "Waiting for Argo CD"

info "Waiting for argocd-server deployment to be available..."
kubectl rollout status deployment/argocd-server \
  -n "${ARGOCD_NAMESPACE}" \
  --timeout=180s
success "Argo CD server is ready."

# ── 6. Apply GitOps Application ───────────────────────────────────────────────
header "GitOps Application"

warn "Argo CD Application requires a public GitHub repository URL."
warn "Edit argocd/application.yaml and set your repoURL, then run:"
warn "  kubectl apply -f argocd/application.yaml -n argocd"
info ""
info "If you want to deploy the local overlay directly (without Argo CD):"
info "  kustomize build kubernetes/overlays/local | kubectl apply -f -"
info ""

# Deploy base manifests directly for local testing
info "Applying Kubernetes manifests via kustomize (local overlay)..."
kustomize build "${PROJECT_ROOT}/kubernetes/overlays/local" | \
  kubectl apply -f - || warn "Some resources may have failed — check above output."

# ── 7. Wait for deployment ────────────────────────────────────────────────────
header "Waiting for Application"

info "Waiting for deployment rollout..."
kubectl rollout status deployment/gitops-demo \
  -n "${NAMESPACE}" \
  --timeout=120s || warn "Deployment not ready — check pod events."

# ── 8. Access information ─────────────────────────────────────────────────────
header "Access Information"

ARGOCD_PASSWORD=$(kubectl -n "${ARGOCD_NAMESPACE}" get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" 2>/dev/null | base64 --decode 2>/dev/null || echo "not-yet-available")

echo -e "${BOLD}Application:${NC}"
echo "  Port-forward : kubectl port-forward svc/gitops-demo 8888:80 -n ${NAMESPACE}"
echo "  Then open    : http://localhost:8888"
echo ""
echo -e "${BOLD}Argo CD UI:${NC}"
echo "  Port-forward : kubectl port-forward svc/argocd-server 8090:443 -n ${ARGOCD_NAMESPACE}"
echo "  Then open    : https://localhost:8090"
echo "  Username     : admin"
echo "  Password     : ${ARGOCD_PASSWORD}"
echo ""
success "Setup complete!"