I fetched and reviewed the repository directly. The repo currently contains a Flask application, Docker setup, Kubernetes base manifests, a local Kustomize overlay, Argo CD configuration, three GitHub Actions workflows, tests, scripts, and architecture documentation. ([GitHub][1])

The actual CI/CD flow is particularly good for a DevOps portfolio: **Git push → CI tests/manifest validation → Docker build → Trivy scan → GHCR push → Kustomize image-tag update → Argo CD synchronization → Kubernetes deployment**. 

One important thing I noticed: the repository still contains placeholder image/repository values such as `ghcr.io/owner/kubernetes-gitops-deployment` and the Argo CD manifest contains `YOUR_GITHUB_USERNAME/...`. You should replace these before presenting the project as fully configured. 

Here is a **detailed, portfolio-quality `README.md`** based specifically on the current repository:

# 🚀 Kubernetes GitOps Deployment System

> **Automated CI/CD and GitOps deployment pipeline using GitHub Actions, Docker, GitHub Container Registry, Kustomize, Argo CD, and Kubernetes.**

[![CI](https://img.shields.io/github/actions/workflow/status/Gauravb741/gitops-kubernetes-deployer/ci.yml?label=CI\&logo=github)](https://github.com/Gauravb741/gitops-kubernetes-deployer/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-326CE5?logo=kubernetes\&logoColor=white)](https://kubernetes.io/)
[![Argo CD](https://img.shields.io/badge/Argo%20CD-GitOps-EF7B4D?logo=argo)](https://argo-cd.readthedocs.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions\&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Overview

**Kubernetes GitOps Deployment System** is a complete DevOps project demonstrating how a containerized application can be automatically tested, built, scanned, published, and deployed to Kubernetes using a **GitOps workflow**.

The project uses **Git as the single source of truth** for application deployment configuration.

Instead of manually running:

```bash
docker build
docker push
kubectl apply
kubectl set image
```

the deployment process is automated.

A developer only needs to push code to GitHub.

The automated pipeline then:

```text
Developer
    │
    │ git push
    ▼
┌──────────────────────┐
│       GitHub         │
│   Source Repository  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    GitHub Actions    │
│                      │
│  • Run tests         │
│  • Lint YAML         │
│  • Validate K8s      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Docker Build      │
│                      │
│  • Build image       │
│  • Trivy scan        │
│  • Generate SBOM     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│        GHCR          │
│ GitHub Container     │
│      Registry        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  GitOps Configuration│
│                      │
│ Update Kustomize     │
│ image SHA tag        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Argo CD        │
│                      │
│ Detect Git change    │
│ Auto Sync + Self Heal│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Kubernetes       │
│                      │
│  Deployment           │
│  Service              │
│  ConfigMap             │
│  Ingress               │
│  Pods                  │
└──────────────────────┘
```

---

# 🎯 Project Goals

The primary goal of this project is to demonstrate a **real-world Kubernetes GitOps deployment workflow** rather than a simple `kubectl apply` deployment.

The project demonstrates:

* Git-based infrastructure management
* Continuous Integration with GitHub Actions
* Automated Python testing
* YAML linting
* Kubernetes manifest validation
* Docker image creation
* Container vulnerability scanning
* GitHub Container Registry integration
* Immutable image tagging using Git SHA
* Kustomize-based Kubernetes configuration
* Argo CD continuous delivery
* Automated synchronization
* Kubernetes health checks
* Rolling updates
* Self-healing deployments
* Container security hardening
* Local Kubernetes development
* Docker Compose based local testing
* Automated cleanup

---

# 🧰 Technology Stack

| Technology                    | Purpose                             |
| ----------------------------- | ----------------------------------- |
| **Python 3.12**               | Application runtime                 |
| **Flask**                     | Web application framework           |
| **Pytest**                    | Automated application testing       |
| **Docker**                    | Application containerization        |
| **Docker Compose**            | Local container development         |
| **GitHub Actions**            | CI/CD automation                    |
| **GitHub Container Registry** | Container image registry            |
| **Trivy**                     | Container vulnerability scanning    |
| **Kubernetes**                | Container orchestration             |
| **Kustomize**                 | Kubernetes configuration management |
| **Argo CD**                   | GitOps continuous delivery          |
| **Kind**                      | Local Kubernetes cluster            |
| **NGINX Ingress**             | Kubernetes ingress routing          |
| **kubeconform**               | Kubernetes manifest validation      |
| **yamllint**                  | YAML linting                        |

---

# ✨ Key Features

## 1. Automated CI Pipeline

Every push and pull request can trigger the CI workflow.

The CI pipeline performs:

### Python tests

```bash
pytest tests/ --tb=short --cov=app
```

### YAML linting

The repository validates Kubernetes manifests and Docker Compose configuration using `yamllint`.

### Kubernetes validation

The project uses `kubeconform` to validate Kubernetes manifests.

### Kustomize validation

The local Kustomize overlay is rendered and validated before deployment.

This prevents invalid configuration from reaching the deployment stage.

---

# 🐳 2. Multi-Stage Docker Build

The application uses a multi-stage Dockerfile.

### Builder stage

```dockerfile
FROM python:3.12-slim AS builder
```

Dependencies are installed separately.

### Runtime stage

```dockerfile
FROM python:3.12-slim AS runtime
```

Only the required runtime files and dependencies are copied into the final image.

The container also:

* Runs as a non-root user
* Uses Python 3.12
* Exposes port `8080`
* Includes a Docker health check
* Uses Gunicorn
* Uses multiple workers
* Enables container-friendly logging

Example runtime command:

```bash
gunicorn \
  --bind 0.0.0.0:8080 \
  --workers 2 \
  --threads 2 \
  --timeout 30 \
  app:app
```

---

# 🔐 3. Container Security

The Docker image does not run the application as root.

A dedicated user is created:

```text
appuser
UID: 1001
GID: 1001
```

Kubernetes also enforces:

```yaml
runAsNonRoot: true
allowPrivilegeEscalation: false
capabilities:
  drop:
    - ALL
```

This reduces the container's privileges and follows common container security practices.

---

# 🔍 4. Trivy Security Scanning

Before the final Docker image is pushed, the workflow scans the image using **Trivy**.

The scan focuses on:

```text
CRITICAL
HIGH
```

severity vulnerabilities.

The results are uploaded to GitHub's security interface in SARIF format.

The workflow also generates:

* Image provenance
* Software Bill of Materials (SBOM)

---

# 📦 5. GitHub Container Registry

Docker images are published to:

```text
ghcr.io/<github-owner>/<repository>
```

Images receive tags based on Git references and Git commit SHA.

The SHA-based tag provides an immutable reference to a specific version of the source code.

Example:

```text
sha-a1b2c3d
```

This is preferable to relying exclusively on:

```text
latest
```

because every deployment can be traced back to a specific Git commit.

---

# 🔄 6. GitOps Deployment

The project follows the GitOps principle:

> **Git is the source of truth for the desired Kubernetes state.**

The deployment configuration is stored inside:

```text
kubernetes/
```

Argo CD monitors the Git repository.

When the deployment configuration changes:

```text
Git change
    ↓
Argo CD detects change
    ↓
Kustomize renders manifests
    ↓
Kubernetes resources updated
```

---

# 🏗️ Architecture

The complete architecture is:

```text
                         ┌────────────────────┐
                         │     Developer      │
                         │                    │
                         │   git push         │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │      GitHub        │
                         │   Source Repo      │
                         └─────────┬──────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
          ┌────────────────────┐      ┌────────────────────┐
          │    CI Workflow     │      │  Docker Workflow   │
          │                    │      │                    │
          │ • Pytest           │      │ • Docker Build     │
          │ • YAML Lint        │      │ • Trivy Scan       │
          │ • K8s Validation   │      │ • GHCR Push        │
          └────────────────────┘      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │       GHCR         │
                                      │ Container Registry │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │ GitOps Workflow    │
                                      │                    │
                                      │ Update Kustomize   │
                                      │ image SHA tag      │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │      Git Repo      │
                                      │ Desired State      │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │      Argo CD       │
                                      │                    │
                                      │ Sync               │
                                      │ Self-Heal          │
                                      │ Prune              │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │    Kubernetes      │
                                      │      Cluster       │
                                      └────────────────────┘
```

---

# 📁 Repository Structure

```text
gitops-kubernetes-deployer/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── docker.yml
│       └── gitops.yml
│
├── app/
│   ├── static/
│   ├── template/
│   ├── app.py
│   └── requirements.txt
│
├── argocd/
│   └── application.yaml
│
├── docker/
│   └── Dockerfile
│
├── docs/
│   └── architecture.md
│
├── kubernetes/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   ├── secret-example.yaml
│   │   └── kustomization.yaml
│   │
│   └── overlays/
│       └── local/
│           └── kustomization.yaml
│
├── scripts/
│   └── cleanup.sh
│
├── tests/
│   └── test_app.py
│
├── .dockerignore
└── docker-compose.yml
```

---

# 🧩 Application

The project contains a Flask application designed specifically to demonstrate Kubernetes and GitOps concepts.

The application exposes several endpoints.

## `/`

Displays the application dashboard.

It provides runtime information such as:

* Application name
* Version
* Environment
* Pod name
* Pod namespace
* Hostname
* Git commit
* Build date
* Uptime
* Request count

---

## `/health`

Kubernetes liveness endpoint.

Example response:

```json
{
  "status": "healthy",
  "timestamp": "..."
}
```

This endpoint is used by Kubernetes to determine whether the application process is alive.

---

## `/ready`

Kubernetes readiness endpoint.

Example:

```json
{
  "status": "ready",
  "timestamp": "..."
}
```

During graceful shutdown the application returns:

```http
503 Service Unavailable
```

This prevents traffic from being routed to a pod that is shutting down.

---

## `/version`

Returns structured application and build information.

Example:

```json
{
  "application": "kubernetes-gitops-demo",
  "version": "1.0.0",
  "environment": "production",
  "pod_name": "...",
  "pod_namespace": "gitops-demo",
  "hostname": "...",
  "git_commit": "...",
  "build_date": "...",
  "uptime_seconds": 123
}
```

---

## `/metrics`

Provides lightweight Prometheus-compatible metrics.

Currently exposed metrics include:

```text
app_uptime_seconds
app_http_requests_total
```

This provides a foundation for integrating the application with a monitoring stack.

---

## `/info`

Provides detailed application and runtime information including:

* Application configuration
* Python version
* Hostname
* Pod metadata
* Uptime
* Request statistics

---

# ☸️ Kubernetes Configuration

The Kubernetes configuration uses a **base + overlay** structure.

```text
kubernetes/
│
├── base/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── kustomization.yaml
│
└── overlays/
    └── local/
        └── kustomization.yaml
```

This makes it possible to reuse the base configuration while applying environment-specific changes.

---

# 🚀 Kubernetes Deployment

The application runs with:

```yaml
replicas: 2
```

The deployment uses:

```text
RollingUpdate
```

with:

```text
maxSurge: 1
maxUnavailable: 0
```

This allows updates to occur without intentionally dropping below the desired number of available replicas.

---

# ❤️ Kubernetes Health Probes

Three different probes are configured.

## Startup Probe

```text
/health
```

Allows the application time to initialize.

## Liveness Probe

```text
/health
```

If the application becomes unhealthy, Kubernetes can restart the container.

## Readiness Probe

```text
/ready
```

Determines whether the pod should receive traffic.

This separation between liveness and readiness is an important Kubernetes production pattern.

---

# 🌐 Kubernetes Service

The application is exposed internally using a:

```text
ClusterIP
```

service.

The service listens on:

```text
Port: 80
```

and forwards traffic to:

```text
Container Port: 8080
```

The local overlay changes the service to:

```text
NodePort
```

using:

```text
30080
```

---

# 🌍 Ingress

The base configuration includes an NGINX Ingress.

The configured hostname is:

```text
gitops-demo.local
```

Requests to:

```text
/
```

are routed to:

```text
gitops-demo
```

service.

---

# 🎨 Kustomize

Kustomize is used to manage Kubernetes configuration without duplicating entire manifests.

The local overlay references:

```yaml
resources:
  - ../../base
```

and applies environment-specific patches.

For example, the local overlay:

* Keeps two replicas
* Changes the service to NodePort
* Assigns NodePort `30080`
* Changes `APP_ENV` to `local-kubernetes`
* Controls the container image tag

---

# 🔁 GitHub Actions Pipeline

The project contains three GitHub Actions workflows.

```text
.github/workflows/

├── ci.yml
├── docker.yml
└── gitops.yml
```

---

# 1️⃣ CI — Test & Validate

File:

```text
.github/workflows/ci.yml
```

Triggered on:

```text
push
pull_request
```

The workflow performs three major jobs.

### Python Tests

```text
Python 3.12
      ↓
Install dependencies
      ↓
Pytest
      ↓
Coverage report
```

Coverage is exported as:

```text
coverage.xml
```

and uploaded as a GitHub Actions artifact.

### YAML Lint

Validates:

```text
kubernetes/
argocd/
docker-compose.yml
```

using `yamllint`.

### Kubernetes Validation

Uses:

```text
kubeconform
```

to validate Kubernetes manifests.

The local Kustomize overlay is also rendered:

```bash
kustomize build kubernetes/overlays/local
```

and passed into kubeconform.

---

# 2️⃣ Docker — Build & Push

File:

```text
.github/workflows/docker.yml
```

Triggered when code is pushed to:

```text
main
master
```

and can also be manually triggered.

Pipeline:

```text
Checkout
   ↓
Docker Buildx
   ↓
Login to GHCR
   ↓
Generate tags
   ↓
Build image
   ↓
Trivy security scan
   ↓
Upload SARIF
   ↓
Build final image
   ↓
Push to GHCR
   ↓
Generate provenance + SBOM
```

---

# 3️⃣ GitOps — Update Deployment

File:

```text
.github/workflows/gitops.yml
```

This workflow runs after the Docker workflow completes successfully.

It calculates the Git commit SHA and creates an immutable image tag:

```text
sha-<commit>
```

It then updates:

```text
kubernetes/overlays/local/kustomization.yaml
```

using:

```bash
kustomize edit set image
```

The workflow commits the updated configuration:

```text
gitops: update image tag to sha-xxxxxxx
```

and pushes the change back to GitHub.

That Git change becomes the trigger for the GitOps deployment.

---

# 🔄 Complete Deployment Flow

The complete automated flow is:

```text
1. Developer modifies application
            │
            ▼
2. git push
            │
            ▼
3. GitHub Actions CI
            │
            ├── Pytest
            ├── Coverage
            ├── YAML lint
            └── Kubernetes validation
            │
            ▼
4. Docker workflow
            │
            ├── Build image
            ├── Trivy scan
            ├── SBOM
            └── Push to GHCR
            │
            ▼
5. GitOps workflow
            │
            └── Update Kustomize image SHA
            │
            ▼
6. Git commit
            │
            ▼
7. Argo CD detects Git change
            │
            ▼
8. Kustomize renders manifests
            │
            ▼
9. Kubernetes receives desired state
            │
            ▼
10. RollingUpdate
            │
            ▼
11. New pods start
            │
            ▼
12. Startup probe passes
            │
            ▼
13. Readiness probe passes
            │
            ▼
14. Traffic routed to new pods
            │
            ▼
15. Old pods terminated
```

---

# 🧭 Argo CD

Argo CD acts as the **Continuous Delivery / GitOps controller**.

The Argo CD application is defined in:

```text
argocd/application.yaml
```

The application watches:

```text
kubernetes/overlays/local
```

and deploys it to:

```text
gitops-demo
```

namespace.

---

# 🔄 Argo CD Self-Healing

The Argo CD configuration enables:

```yaml
automated:
  prune: true
  selfHeal: true
```

### Prune

Resources removed from Git can be removed from the Kubernetes cluster.

### Self-Heal

If somebody manually changes a Kubernetes resource:

```text
Git desired state
       │
       │ differs
       ▼
Kubernetes actual state
```

Argo CD can detect the drift and reconcile the cluster back to the state defined in Git.

This is one of the major benefits of the GitOps model.

---

# 🧪 Local Development

## Prerequisites

Install:

* Git
* Docker
* Docker Compose
* Python 3.12
* kubectl
* Kind
* Kustomize
* Argo CD

Optional:

* NGINX Ingress Controller
* Trivy
* kubeconform
* yamllint

---

# 🐍 Run Application Locally

Clone the repository:

```bash
git clone https://github.com/Gauravb741/gitops-kubernetes-deployer.git
```

Enter the directory:

```bash
cd gitops-kubernetes-deployer
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r app/requirements.txt
```

Run the application:

```bash
python app/app.py
```

The application listens on:

```text
http://localhost:8080
```

---

# 🐳 Run With Docker Compose

The repository includes a Docker Compose configuration for local development.

Run:

```bash
docker compose up --build
```

The application becomes available at:

```text
http://localhost:8080
```

Stop the application:

```bash
docker compose down
```

Run in detached mode:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

---

# ☸️ Run With Kubernetes

Create a local Kind cluster:

```bash
kind create cluster --name gitops-demo
```

Verify:

```bash
kubectl cluster-info
```

Check nodes:

```bash
kubectl get nodes
```

---

# 🔧 Build Kubernetes Configuration

Render the Kustomize overlay:

```bash
kustomize build kubernetes/overlays/local
```

You can inspect the generated Kubernetes resources before applying them.

---

# 🚀 Deploy Manually

Apply the local overlay:

```bash
kubectl apply -k kubernetes/overlays/local
```

Check namespace:

```bash
kubectl get namespaces
```

Check deployments:

```bash
kubectl get deployments -n gitops-demo
```

Check pods:

```bash
kubectl get pods -n gitops-demo
```

Check services:

```bash
kubectl get services -n gitops-demo
```

Check ingress:

```bash
kubectl get ingress -n gitops-demo
```

---

# 🌐 Access the Application

The local overlay exposes the application using NodePort:

```text
30080
```

You can inspect the service:

```bash
kubectl get svc -n gitops-demo
```

Depending on the Kind networking configuration, you can access the application using the appropriate local port-forward or Kind networking method.

A simple approach is:

```bash
kubectl port-forward svc/gitops-demo 8080:80 -n gitops-demo
```

Then open:

```text
http://localhost:8080
```

---

# 🔱 Install Argo CD

Create the Argo CD namespace:

```bash
kubectl create namespace argocd
```

Install Argo CD using the official installation method.

After installation, verify:

```bash
kubectl get pods -n argocd
```

Wait until the Argo CD components are ready.

---

# ⚙️ Configure Argo CD

Before applying:

```text
argocd/application.yaml
```

make sure the repository URL points to the actual repository.

The configuration should reference:

```text
https://github.com/Gauravb741/gitops-kubernetes-deployer.git
```

The application should point to:

```text
kubernetes/overlays/local
```

Then apply:

```bash
kubectl apply -f argocd/application.yaml -n argocd
```

Check the application:

```bash
kubectl get applications -n argocd
```

---

# 🔍 Verify GitOps Synchronization

After Argo CD is configured:

```bash
kubectl get application gitops-demo -n argocd
```

You should eventually see the application become synchronized and healthy.

The expected GitOps flow is:

```text
Git Repository
      ↓
Argo CD
      ↓
Kustomize
      ↓
Kubernetes
      ↓
Deployment
      ↓
Pods
```

---

# 🩺 Application Health Checks

Check pod status:

```bash
kubectl get pods -n gitops-demo
```

Check pod details:

```bash
kubectl describe pod <pod-name> -n gitops-demo
```

Check application logs:

```bash
kubectl logs -n gitops-demo deployment/gitops-demo
```

Test health:

```bash
kubectl port-forward svc/gitops-demo 8080:80 -n gitops-demo
```

Then:

```bash
curl http://localhost:8080/health
```

Test readiness:

```bash
curl http://localhost:8080/ready
```

Test version:

```bash
curl http://localhost:8080/version
```

Test metrics:

```bash
curl http://localhost:8080/metrics
```

---

# 🧹 Cleanup

The repository includes:

```text
scripts/cleanup.sh
```

The script removes:

* Application namespace
* Argo CD application

The Kind cluster is preserved by default.

Run:

```bash
bash scripts/cleanup.sh
```

To also delete the Kind cluster:

```bash
DELETE_CLUSTER=true bash scripts/cleanup.sh
```

Or manually:

```bash
kind delete cluster --name gitops-demo
```

---

# 🔐 Secrets

The repository contains:

```text
kubernetes/base/secret-example.yaml
```

but the example secret is intentionally excluded from the default Kustomize deployment.

For production environments, secrets should be managed using an appropriate secret-management solution rather than committing sensitive credentials directly to Git.

Possible production approaches include:

* External Secrets Operator
* Sealed Secrets
* HashiCorp Vault
* Cloud provider secret managers
* SOPS

---

# 🧪 Testing

Run the complete test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ \
  --cov=app \
  --cov-report=term-missing
```

The same testing process is automatically executed by GitHub Actions.

---

# 🛡️ Security Practices

This project implements several security-conscious practices.

### Container

```text
✓ Non-root user
✓ Minimal Python slim image
✓ Multi-stage build
✓ Docker health check
✓ No unnecessary Linux capabilities
```

### Kubernetes

```text
✓ runAsNonRoot
✓ Non-root UID
✓ Non-root GID
✓ RuntimeDefault seccomp profile
✓ allowPrivilegeEscalation disabled
✓ Linux capabilities dropped
✓ Resource requests
✓ Resource limits
```

### CI/CD

```text
✓ Trivy vulnerability scanning
✓ SARIF security reports
✓ Immutable SHA image tags
✓ SBOM generation
✓ GitHub Actions permissions
```

---

# 📊 Observability

The application provides basic observability features.

## Structured Logging

Application logs are emitted in JSON-compatible structured format.

Example:

```json
{
  "timestamp": "...",
  "level": "INFO",
  "logger": "gitops-demo",
  "message": "HTTP request processed"
}
```

This format is suitable for log aggregation systems.

---

# 📈 Metrics

The application provides:

```text
/metrics
```

with metrics such as:

```text
app_uptime_seconds
app_http_requests_total
```

These can be consumed by monitoring systems such as Prometheus.

---

# 🏷️ Image Versioning Strategy

The deployment pipeline uses Git commit SHA based image tags.

Example:

```text
sha-7f83a1b
```

This provides:

### Traceability

Every deployed image can be mapped to a Git commit.

### Reproducibility

A specific image version can be deployed again.

### Safer rollbacks

Instead of guessing which `latest` image was deployed, the exact image tag can be selected.

---

# 🔙 Rollback Strategy

Because deployments use immutable SHA-based image tags, rollback can be performed by changing the Kustomize image tag back to a previously known-good SHA.

Example:

```text
Current:

sha-a1b2c3d

Rollback:

sha-91f4e2a
```

After committing the configuration change:

```text
Git
 ↓
Argo CD
 ↓
Kustomize
 ↓
Kubernetes
```

The previous application version is restored.

---

# 🔄 GitOps vs Traditional Deployment

## Traditional Kubernetes Deployment

```text
Developer
   ↓
Build Image
   ↓
Push Image
   ↓
kubectl apply
   ↓
Kubernetes
```

This approach requires manual deployment operations.

---

## GitOps Deployment

```text
Developer
   ↓
Git Push
   ↓
GitHub Actions
   ↓
Build + Scan + Push
   ↓
Update Git Configuration
   ↓
Argo CD
   ↓
Kubernetes
```

The cluster continuously reconciles itself against the desired state stored in Git.

---

# 💡 Why This Project Matters

This project demonstrates several concepts commonly used in modern DevOps and Platform Engineering environments.

Instead of demonstrating Kubernetes in isolation, it connects multiple tools into one complete workflow:

```text
Linux
  ↓
Git
  ↓
GitHub
  ↓
GitHub Actions
  ↓
Docker
  ↓
Container Registry
  ↓
Kubernetes
  ↓
Kustomize
  ↓
Argo CD
  ↓
GitOps
```

It therefore serves as a practical demonstration of:

* CI/CD
* Containerization
* Infrastructure configuration
* Kubernetes orchestration
* GitOps
* Continuous Delivery
* Security scanning
* Configuration management
* Deployment automation
* Observability
* DevOps automation

---

# 🧑‍💻 Skills Demonstrated

A developer working with this project can demonstrate knowledge of:

### Linux

```text
Shell scripting
Process management
CLI tooling
Environment variables
```

### Git & GitHub

```text
Branches
Commits
Pull requests
Repository workflows
GitHub Actions
```

### CI/CD

```text
Automated testing
Build pipelines
Artifact generation
Deployment automation
Workflow dependencies
```

### Docker

```text
Dockerfiles
Multi-stage builds
Container security
Docker Compose
Health checks
Image tagging
```

### Kubernetes

```text
Pods
Deployments
Services
ConfigMaps
Ingress
Namespaces
Probes
Resource limits
Security contexts
Rolling updates
```

### Kustomize

```text
Bases
Overlays
Patches
Image replacement
Environment-specific configuration
```

### GitOps

```text
Declarative deployment
Desired state
Continuous reconciliation
Self-healing
Automated synchronization
Configuration as code
```

### Argo CD

```text
Applications
Automated sync
Pruning
Self-healing
Git-based deployment
```

---

# 🗺️ Future Improvements

Possible extensions include:

* Prometheus monitoring
* Grafana dashboards
* Alertmanager integration
* Horizontal Pod Autoscaler
* NetworkPolicies
* PodDisruptionBudgets
* External Secrets Operator
* TLS with cert-manager
* Multiple environments
* Development / staging / production overlays
* Blue-green deployments
* Canary deployments
* Argo Rollouts
* Image signing
* Cosign
* Policy enforcement
* OPA Gatekeeper
* Kyverno
* SAST integration
* Dependency scanning
* GitHub Dependabot
* Kubernetes dashboard
* Cloud deployment to AWS EKS
* Infrastructure provisioning using Terraform

---

# 🌎 Multi-Environment Extension

The current repository uses:

```text
kubernetes/base
kubernetes/overlays/local
```

This structure can naturally be expanded to:

```text
kubernetes/
│
├── base/
│
└── overlays/
    ├── local/
    ├── development/
    ├── staging/
    └── production/
```

Each environment can maintain its own:

* Replica count
* Image tag
* Resource limits
* Environment variables
* Ingress hostname
* Service configuration
* Scaling configuration

while sharing the same Kubernetes base.

---

# 🏆 Portfolio Value

This project is suitable for demonstrating practical DevOps skills because it goes beyond simply deploying a Docker container.

It demonstrates an end-to-end engineering workflow:

```text
SOURCE CODE
    ↓
VERSION CONTROL
    ↓
CONTINUOUS INTEGRATION
    ↓
AUTOMATED TESTING
    ↓
CONTAINER BUILD
    ↓
SECURITY SCANNING
    ↓
CONTAINER REGISTRY
    ↓
GITOPS CONFIGURATION
    ↓
CONTINUOUS DELIVERY
    ↓
KUBERNETES
    ↓
HEALTH CHECKS
    ↓
SELF-HEALING
```

---

# 📚 Learning Outcomes

After working with this project, you should understand:

1. How Docker images are built and published.
2. How GitHub Actions automates CI/CD.
3. How container vulnerability scanning works.
4. How Git SHA tags provide immutable image versions.
5. How Kubernetes Deployments perform rolling updates.
6. Why liveness and readiness probes are different.
7. How Kustomize manages Kubernetes configurations.
8. How Argo CD implements GitOps.
9. How Git becomes the source of truth for deployments.
10. How Kubernetes automatically maintains desired state.
11. How configuration drift can be detected and corrected.
12. How security can be integrated into a CI/CD pipeline.

---

# 🧾 Project Status

| Component                   | Status      |
| --------------------------- | ----------- |
| Flask application           | ✅           |
| Docker containerization     | ✅           |
| Docker Compose              | ✅           |
| Python tests                | ✅           |
| GitHub Actions CI           | ✅           |
| YAML validation             | ✅           |
| Kubernetes validation       | ✅           |
| GHCR integration            | ✅           |
| Trivy scanning              | ✅           |
| Kustomize                   | ✅           |
| Argo CD configuration       | ✅           |
| Kubernetes deployment       | ✅           |
| Health probes               | ✅           |
| GitOps image update         | ✅           |
| Automated cleanup           | ✅           |
| Production cloud deployment | 🔧 Optional |
| Monitoring stack            | 🔧 Optional |

---

# ⚠️ Configuration Before Deployment

Before using this repository with your own GitHub account, review the following values:

### Argo CD repository URL

Update:

```text
argocd/application.yaml
```

from the placeholder repository URL to your actual repository.

### Container image

Review:

```text
kubernetes/base/deployment.yaml
```

and:

```text
kubernetes/overlays/local/kustomization.yaml
```

for placeholder image names.

The repository currently contains values such as:

```text
ghcr.io/owner/kubernetes-gitops-deployment
```

which should be changed to the actual GitHub Container Registry image for your repository.

---

# 🤝 Contributing

Contributions are welcome.

A typical contribution workflow is:

```bash
git checkout -b feature/my-change
```

Make your changes, run tests:

```bash
pytest tests/ -v
```

Validate Kubernetes configuration:

```bash
kustomize build kubernetes/overlays/local
```

Commit:

```bash
git add .
git commit -m "feat: add my change"
```

Push:

```bash
git push origin feature/my-change
```

Then create a Pull Request.

---

# 📄 License

This project is released under the **MIT License**.

See the `LICENSE` file for details.

---

# 👨‍💻 Author

**Gaurav B.**

GitHub:

```text
https://github.com/Gauravb741
```

Repository:

```text
https://github.com/Gauravb741/gitops-kubernetes-deployer
```

---

# ⭐ If You Find This Project Useful

If this project helped you understand GitOps, Kubernetes, Docker, or CI/CD:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Open an issue
* 💡 Suggest improvements
* 🤝 Contribute

---

## 🚀 Quick Summary

```text
┌─────────────────────────────────────────────────────────────┐
│              KUBERNETES GITOPS DEPLOYMENT                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GitHub                                                     │
│     │                                                       │
│     ▼                                                       │
│  GitHub Actions                                             │
│     │                                                       │
│     ├── Tests                                                │
│     ├── YAML Validation                                      │
│     ├── Kubernetes Validation                                │
│     │                                                       │
│     ▼                                                       │
│  Docker                                                     │
│     │                                                       │
│     ├── Build                                                │
│     ├── Trivy Scan                                           │
│     ├── SBOM                                                 │
│     │                                                       │
│     ▼                                                       │
│  GHCR                                                       │
│     │                                                       │
│     ▼                                                       │
│  Kustomize                                                   │
│     │                                                       │
│     ├── Immutable SHA image                                  │
│     │                                                       │
│     ▼                                                       │
│  Git Commit                                                  │
│     │                                                       │
│     ▼                                                       │
│  Argo CD                                                     │
│     │                                                       │
│     ├── Auto Sync                                            │
│     ├── Self Heal                                            │
│     └── Prune                                                │
│     │                                                       │
│     ▼                                                       │
│  Kubernetes                                                  │
│     │                                                       │
│     ├── Deployment                                           │
│     ├── Service                                              │
│     ├── ConfigMap                                            │
│     ├── Ingress                                              │
│     └── Pods                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Git → CI → Docker → Security Scan → Registry → GitOps → Argo CD → Kubernetes**

That's the complete deployment lifecycle implemented by this project.

[1]: https://github.com/Gauravb741/gitops-kubernetes-deployer "GitHub - Gauravb741/gitops-kubernetes-deployer · GitHub"
