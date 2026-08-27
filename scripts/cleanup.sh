#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  cleanup.sh — Remove locally created resources
# ══════════════════════════════════════════════════════════════════════════════
set -uo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'; BOLD='\033[1m'

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }

CLUSTER_NAME="${CLUSTER_NAME:-gitops-demo}"
NAMESPACE="${NAMESPACE:-gitops-demo}"
DELETE_CLUSTER="${DELETE_CLUSTER:-false}"

echo -e "\n${BOLD}Cleanup — Kubernetes GitOps Demo${NC}"
echo "════════════════════════════════"

# ── Remove application namespace ──────────────────────────────────────────────
if kubectl get namespace "${NAMESPACE}" &>/dev/null; then
  info "Deleting namespace '${NAMESPACE}' and all its resources..."
  kubectl delete namespace "${NAMESPACE}" --timeout=60s || \
    warn "Namespace deletion timed out — it will finish in the background."
  success "Namespace '${NAMESPACE}' deleted."
else
  info "Namespace '${NAMESPACE}' does not exist — nothing to delete."
fi

# ── Remove Argo CD Application ────────────────────────────────────────────────
if kubectl get application gitops-demo -n argocd &>/dev/null; then
  info "Removing Argo CD Application 'gitops-demo'..."
  kubectl delete application gitops-demo -n argocd || true
  success "Argo CD Application removed."
fi

# ── Optionally delete Kind cluster ────────────────────────────────────────────
if [[ "${DELETE_CLUSTER}" == "true" ]]; then
  if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    info "Deleting Kind cluster '${CLUSTER_NAME}'..."
    kind delete cluster --name "${CLUSTER_NAME}"
    success "Kind cluster deleted."
  else
    info "Kind cluster '${CLUSTER_NAME}' does not exist."
  fi
else
  warn "Kind cluster '${CLUSTER_NAME}' was NOT deleted."
  warn "To delete it, run: DELETE_CLUSTER=true bash scripts/cleanup.sh"
  warn "Or manually:        kind delete cluster --name ${CLUSTER_NAME}"
fi

echo ""
success "Cleanup complete."