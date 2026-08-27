#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  verify.sh — Comprehensive cluster and application health check
# ══════════════════════════════════════════════════════════════════════════════
set -uo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'; BOLD='\033[1m'

PASS=0; FAIL=0

check() {
  local description="$1"
  local command="$2"
  if eval "${command}" &>/dev/null; then
    echo -e "${GREEN}✓${NC} ${description}"
    PASS=$((PASS + 1))
  else
    echo -e "${RED}✗${NC} ${description}"
    FAIL=$((FAIL + 1))
  fi
}

warn_check() {
  local description="$1"
  local command="$2"
  if eval "${command}" &>/dev/null; then
    echo -e "${GREEN}✓${NC} ${description}"
    PASS=$((PASS + 1))
  else
    echo -e "${YELLOW}⚠${NC} ${description} (optional)"
  fi
}

NAMESPACE="${NAMESPACE:-gitops-demo}"
ARGOCD_NS="argocd"

echo -e "\n${BOLD}Kubernetes GitOps Demo — Verification Report${NC}"
echo "════════════════════════════════════════════"

# ── Cluster ───────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ Cluster Connectivity${NC}"
check "kubectl can reach the cluster" "kubectl cluster-info"

# ── Namespace ─────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ Namespace${NC}"
check "Namespace '${NAMESPACE}' exists" \
  "kubectl get namespace ${NAMESPACE}"

# ── Deployment ────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ Deployment${NC}"
check "Deployment 'gitops-demo' exists" \
  "kubectl get deployment gitops-demo -n ${NAMESPACE}"
check "Deployment has at least 1 ready replica" \
  "kubectl get deployment gitops-demo -n ${NAMESPACE} -o jsonpath='{.status.readyReplicas}' | grep -E '^[1-9]'"

# ── Pods ──────────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ Pods${NC}"
check "At least one pod is Running" \
  "kubectl get pods -n ${NAMESPACE} -l app=gitops-demo --field-selector=status.phase=Running | grep Running"

# ── Service ───────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ Service${NC}"
check "Service 'gitops-demo' exists" \
  "kubectl get service gitops-demo -n ${NAMESPACE}"

# ── ConfigMap ─────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ ConfigMap${NC}"
check "ConfigMap 'gitops-demo-config' exists" \
  "kubectl get configmap gitops-demo-config -n ${NAMESPACE}"

# ── Ingress ───────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ Ingress${NC}"
warn_check "Ingress 'gitops-demo' exists" \
  "kubectl get ingress gitops-demo -n ${NAMESPACE}"

# ── Argo CD ───────────────────────────────────────────────────────────────────
echo -e "\n${BLUE}▶ Argo CD${NC}"
warn_check "Argo CD namespace exists" \
  "kubectl get namespace ${ARGOCD_NS}"
warn_check "argocd-server is running" \
  "kubectl get deployment argocd-server -n ${ARGOCD_NS}"
warn_check "GitOps Application 'gitops-demo' exists" \
  "kubectl get application gitops-demo -n ${ARGOCD_NS}"

# ── Application health via port-forward ───────────────────────────────────────
echo -e "\n${BLUE}▶ Application Endpoints${NC}"

# Attempt a quick port-forward test
POD=$(kubectl get pod -n "${NAMESPACE}" -l app=gitops-demo \
  -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

if [[ -n "${POD}" ]]; then
  # Start port-forward in background
  kubectl port-forward "pod/${POD}" 19876:8080 -n "${NAMESPACE}" &>/dev/null &
  PF_PID=$!
  sleep 3

  check "/health returns HTTP 200" \
    "curl -sf http://localhost:19876/health | grep healthy"
  check "/ready returns HTTP 200" \
    "curl -sf http://localhost:19876/ready | grep ready"
  check "/version returns application info" \
    "curl -sf http://localhost:19876/version | grep kubernetes-gitops-demo"

  kill "${PF_PID}" 2>/dev/null || true
else
  echo -e "${YELLOW}⚠${NC} No running pods found — skipping endpoint checks."
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════"
echo -e "${BOLD}Results: ${GREEN}${PASS} passed${NC}  ${RED}${FAIL} failed${NC}"
echo "════════════════════════════════════════════"

if [[ ${FAIL} -gt 0 ]]; then
  exit 1
fi