#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  deploy.sh — Apply the Kustomize overlay to the cluster
# ══════════════════════════════════════════════════════════════════════════════
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; NC='\033[0m'; BOLD='\033[1m'
info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
NAMESPACE="${NAMESPACE:-gitops-demo}"
OVERLAY="${OVERLAY:-local}"

info "Building and applying overlay: ${OVERLAY}"
kustomize build "${PROJECT_ROOT}/kubernetes/overlays/${OVERLAY}" \
  | kubectl apply -f -

info "Waiting for rollout..."
kubectl rollout status deployment/gitops-demo \
  -n "${NAMESPACE}" --timeout=120s

success "Deployment complete."

info "Pod status:"
kubectl get pods -n "${NAMESPACE}" -l app=gitops-demo