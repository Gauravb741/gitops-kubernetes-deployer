# Architecture

## Overview

The Kubernetes GitOps Deployment System implements a fully automated pipeline where every code change flows from a developer's workstation to a production-equivalent Kubernetes cluster without any manual intervention in the deployment process.

## System Architecture Diagram

```mermaid
flowchart TD
    DEV[👨‍💻 Developer\nLocal Workstation]

    subgraph GitHub["🐙 GitHub"]
        REPO[Git Repository\nSource of Truth]
        ACTIONS[GitHub Actions\nCI/CD Engine]
    end

    subgraph Registry["📦 Container Registry"]
        GHCR[GHCR\nghcr.io/owner/repo]
    end

    subgraph GitOps["🔄 GitOps Layer"]
        KUSTOMIZE[Kustomize\nConfiguration Management]
        ARGOCD[Argo CD\nContinuous Delivery]
    end

    subgraph K8S["⎈ Kubernetes Cluster"]
        NS[Namespace: gitops-demo]
        DEP[Deployment\n2 Replicas]
        SVC[Service\nClusterIP]
        CM[ConfigMap]
        ING[Ingress]

        subgraph PODS["Pods"]
            P1[Pod 1\n/health ✓\n/ready ✓]
            P2[Pod 2\n/health ✓\n/ready ✓]
        end
    end

    DEV -->|git push| REPO
    REPO --> ACTIONS

    ACTIONS -->|1. Run Tests| ACTIONS
    ACTIONS -->|2. Build Image| GHCR
    ACTIONS -->|3. Update kustomization.yaml| REPO

    REPO -->|Watch for changes| ARGOCD
    ARGOCD --> KUSTOMIZE
    KUSTOMIZE -->|kubectl apply| K8S

    K8S --> NS
    NS --> DEP
    NS --> SVC
    NS --> CM
    NS --> ING
    DEP --> PODS

    classDef github fill:#24292e,color:#fff
    classDef registry fill:#0e4c96,color:#fff
    classDef gitops fill:#ef7b4d,color:#fff
    classDef k8s fill:#326ce5,color:#fff