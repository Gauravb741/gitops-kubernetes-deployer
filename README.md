# 🚀 Kubernetes GitOps Deployment System

A complete **CI/CD and GitOps deployment system** that automatically builds, tests, scans, and deploys a containerized application to Kubernetes.

The project combines:

* GitHub
* GitHub Actions
* Docker
* GitHub Container Registry
* Kubernetes
* Kustomize
* Argo CD
* Trivy
* Pytest

The main objective is to create an automated deployment pipeline where **Git acts as the source of truth for Kubernetes deployments**.

---

## 📌 Overview

The project implements an automated workflow:

```text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Run Tests
    ├── YAML Validation
    └── Kubernetes Validation
    │
    ▼
Docker Build
    │
    ├── Build Image
    ├── Security Scan
    └── Generate SBOM
    │
    ▼
GitHub Container Registry
    │
    ▼
GitOps Configuration Update
    │
    ▼
Git Repository
    │
    ▼
Argo CD
    │
    ├── Detect Changes
    ├── Synchronize
    └── Self-Heal
    │
    ▼
Kubernetes
    │
    ├── Deployment
    ├── Service
    ├── ConfigMap
    └── Ingress
```

Once the application code is pushed to GitHub, the rest of the deployment process is automated.

---

# 🛠️ Technology Stack

| Technology                | Purpose                        |
| ------------------------- | ------------------------------ |
| Python 3.12               | Application runtime            |
| Flask                     | Web application                |
| Pytest                    | Automated testing              |
| Docker                    | Containerization               |
| Docker Compose            | Local development              |
| GitHub Actions            | CI/CD                          |
| GitHub Container Registry | Container image storage        |
| Trivy                     | Container security scanning    |
| Kubernetes                | Container orchestration        |
| Kustomize                 | Kubernetes configuration       |
| Argo CD                   | GitOps deployment              |
| Kind                      | Local Kubernetes cluster       |
| NGINX Ingress             | Application routing            |
| kubeconform               | Kubernetes manifest validation |
| yamllint                  | YAML validation                |

---

# ✨ Features

* Automated CI pipeline
* Automated Python testing
* Code coverage
* YAML linting
* Kubernetes manifest validation
* Docker image building
* Multi-stage Docker build
* Container vulnerability scanning
* SBOM generation
* GitHub Container Registry integration
* Immutable Git SHA image tags
* Kubernetes deployments
* Kubernetes health checks
* Liveness probes
* Readiness probes
* Startup probes
* Kustomize overlays
* Argo CD deployment
* Automatic synchronization
* Automatic pruning
* Self-healing
* Rolling updates
* Non-root containers
* Kubernetes security contexts
* Local Kubernetes development
* Docker Compose development
* Automated cleanup

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      Developer      │
                         │                     │
                         │      git push       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       GitHub        │
                         │   Source Repository │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
          ┌─────────────────────┐       ┌─────────────────────┐
          │   GitHub Actions    │       │   Docker Pipeline   │
          │                     │       │                     │
          │ • Pytest            │       │ • Build             │
          │ • YAML Lint         │       │ • Trivy Scan        │
          │ • K8s Validation    │       │ • SBOM              │
          └─────────────────────┘       └──────────┬──────────┘
                                                   │
                                                   ▼
                                        ┌─────────────────────┐
                                        │        GHCR         │
                                        │ Container Registry  │
                                        └──────────┬──────────┘
                                                   │
                                                   ▼
                                        ┌─────────────────────┐
                                        │   GitOps Workflow   │
                                        │                     │
                                        │ Update image SHA    │
                                        └──────────┬──────────┘
                                                   │
                                                   ▼
                                        ┌─────────────────────┐
                                        │    Git Repository   │
                                        │   Desired State     │
                                        └──────────┬──────────┘
                                                   │
                                                   ▼
                                        ┌─────────────────────┐
                                        │       Argo CD       │
                                        │                     │
                                        │ • Sync              │
                                        │ • Self-Heal         │
                                        │ • Prune             │
                                        └──────────┬──────────┘
                                                   │
                                                   ▼
                                        ┌─────────────────────┐
                                        │     Kubernetes      │
                                        │                     │
                                        │ Deployment          │
                                        │ Service             │
                                        │ ConfigMap           │
                                        │ Ingress             │
                                        │ Pods                │
                                        └─────────────────────┘
```

---

# 📁 Project Structure

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

# 🔄 CI/CD Pipeline

The project uses three GitHub Actions workflows:

```text
.github/workflows/

├── ci.yml
├── docker.yml
└── gitops.yml
```

---

## 1. CI Workflow

The CI workflow validates the application before it is deployed.

```text
Git Push / Pull Request
          │
          ▼
     Run Pytest
          │
          ▼
     Generate Coverage
          │
          ▼
      YAML Lint
          │
          ▼
 Kubernetes Validation
          │
          ▼
     Kustomize Build
```

### Python Tests

```bash
pytest tests/ --tb=short --cov=app
```

The workflow also generates a coverage report.

---

## YAML Validation

The repository uses `yamllint` to validate configuration files.

The validation covers:

```text
kubernetes/
argocd/
docker-compose.yml
```

---

## Kubernetes Validation

Kubernetes manifests are validated using `kubeconform`.

The local Kustomize overlay is rendered before validation:

```bash
kustomize build kubernetes/overlays/local
```

This helps detect invalid Kubernetes configuration before deployment.

---

# 🐳 Docker

The application is containerized using a multi-stage Docker build.

The Docker image uses:

```text
Python 3.12 Slim
```

The runtime container:

* Uses a non-root user
* Exposes port `8080`
* Includes a health check
* Uses Gunicorn
* Uses multiple workers
* Uses a minimal runtime image

Example application command:

```bash
gunicorn \
  --bind 0.0.0.0:8080 \
  --workers 2 \
  --threads 2 \
  --timeout 30 \
  app:app
```

---

# 🔐 Container Security

The container does not run as root.

The application uses a dedicated user:

```text
appuser
UID: 1001
GID: 1001
```

Kubernetes additionally applies:

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
```

Linux capabilities are also dropped:

```yaml
capabilities:
  drop:
    - ALL
```

---

# 🔍 Trivy Security Scanning

The Docker pipeline uses Trivy to scan the container image for vulnerabilities.

The pipeline checks:

```text
HIGH
CRITICAL
```

severity vulnerabilities.

Security results are uploaded to GitHub's security interface.

The pipeline also generates an SBOM for the image.

---

# 📦 GitHub Container Registry

Built Docker images are pushed to:

```text
ghcr.io/<github-owner>/<repository>
```

Images are tagged using Git information.

The most important tag is the Git SHA:

```text
sha-<commit>
```

For example:

```text
sha-a1b2c3d
```

This makes every deployed container traceable to a specific Git commit.

---

# 🔄 GitOps Workflow

After the Docker image is successfully built and pushed, the GitOps workflow updates the Kubernetes configuration.

The image reference is updated in:

```text
kubernetes/overlays/local/kustomization.yaml
```

The workflow uses Kustomize:

```bash
kustomize edit set image
```

The updated configuration is committed back to Git.

Example commit:

```text
gitops: update image tag to sha-a1b2c3d
```

This Git change is then detected by Argo CD.

---

# 🔱 Argo CD

Argo CD continuously monitors the Git repository.

The basic flow is:

```text
Git Repository
      │
      ▼
   Argo CD
      │
      ▼
  Kustomize
      │
      ▼
 Kubernetes
```

Argo CD is responsible for keeping the Kubernetes cluster synchronized with the desired state stored in Git.

---

# 🔄 Self-Healing

The Argo CD configuration enables:

```yaml
automated:
  prune: true
  selfHeal: true
```

### Self-Heal

If a Kubernetes resource is manually modified, Argo CD can detect the difference between:

```text
Git State
   vs
Cluster State
```

and restore the cluster to the state defined in Git.

### Pruning

Resources removed from the Git configuration can also be removed from the Kubernetes cluster.

---

# ☸️ Kubernetes

The Kubernetes configuration follows a **Base + Overlay** structure.

```text
kubernetes/
│
├── base/
│
└── overlays/
    └── local/
```

This allows common Kubernetes configuration to be stored in the base while environment-specific configuration is maintained in overlays.

---

# 🚀 Kubernetes Deployment

The application runs with:

```text
Replicas: 2
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

This allows new pods to be created before old pods are removed.

---

# ❤️ Health Probes

The application provides three Kubernetes probes.

## Startup Probe

```text
/health
```

Used during application startup.

## Liveness Probe

```text
/health
```

Used to determine whether the application is still running correctly.

## Readiness Probe

```text
/ready
```

Used to determine whether the pod should receive traffic.

If the application is shutting down, the readiness endpoint can return:

```text
503 Service Unavailable
```

which prevents traffic from being sent to the terminating pod.

---

# 🌐 Kubernetes Service

The application uses a Kubernetes `ClusterIP` service in the base configuration.

The service exposes:

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

The Kubernetes configuration includes an NGINX Ingress.

The configured host is:

```text
gitops-demo.local
```

Traffic is routed to the application service.

---

# 🧩 Application Endpoints

The Flask application provides several endpoints.

## `/`

Main application dashboard.

Displays application and runtime information.

---

## `/health`

Health endpoint.

Example:

```json
{
  "status": "healthy"
}
```

---

## `/ready`

Readiness endpoint.

Example:

```json
{
  "status": "ready"
}
```

---

## `/version`

Returns application and build information.

Example:

```json
{
  "application": "kubernetes-gitops-demo",
  "version": "1.0.0",
  "environment": "production",
  "pod_name": "...",
  "pod_namespace": "...",
  "git_commit": "...",
  "build_date": "..."
}
```

---

## `/metrics`

Provides basic metrics such as:

```text
app_uptime_seconds
app_http_requests_total
```

---

## `/info`

Provides runtime and application information.

---

# 💻 Local Development

## Requirements

Install:

* Git
* Python 3.12
* Docker
* Docker Compose
* kubectl
* Kind
* Kustomize

For the complete GitOps workflow, also install:

* Argo CD
* Trivy
* kubeconform
* yamllint

---

# 🐍 Run With Python

Clone the repository:

```bash
git clone https://github.com/Gauravb741/gitops-kubernetes-deployer.git
```

Enter the project:

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

Run:

```bash
python app/app.py
```

Application:

```text
http://localhost:8080
```

---

# 🐳 Run With Docker Compose

Build and start:

```bash
docker compose up --build
```

Run in background:

```bash
docker compose up --build -d
```

Check containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

Application:

```text
http://localhost:8080
```

---

# ☸️ Run With Kubernetes

Create a Kind cluster:

```bash
kind create cluster --name gitops-demo
```

Check the cluster:

```bash
kubectl cluster-info
```

Check nodes:

```bash
kubectl get nodes
```

---

# 🔧 Validate Kustomize

Render the Kubernetes configuration:

```bash
kustomize build kubernetes/overlays/local
```

This allows you to inspect the final Kubernetes manifests before deploying them.

---

# 🚀 Deploy to Kubernetes

Apply the configuration:

```bash
kubectl apply -k kubernetes/overlays/local
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

A simple way to access the application locally is port forwarding:

```bash
kubectl port-forward svc/gitops-demo 8080:80 -n gitops-demo
```

Then open:

```text
http://localhost:8080
```

Test the health endpoint:

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

# 🔱 Configure Argo CD

Create the Argo CD namespace:

```bash
kubectl create namespace argocd
```

Install Argo CD using its standard installation method.

Verify:

```bash
kubectl get pods -n argocd
```

Before applying the Argo CD application configuration, make sure:

```text
argocd/application.yaml
```

points to the correct Git repository.

Then apply:

```bash
kubectl apply -f argocd/application.yaml -n argocd
```

Check the application:

```bash
kubectl get applications -n argocd
```

---

# 🔄 Complete GitOps Flow

The complete deployment process is:

```text
1. Developer changes code
          │
          ▼
2. git push
          │
          ▼
3. GitHub Actions
          │
          ├── Run tests
          ├── Validate YAML
          └── Validate Kubernetes
          │
          ▼
4. Docker image build
          │
          ▼
5. Trivy security scan
          │
          ▼
6. Push image to GHCR
          │
          ▼
7. GitOps workflow updates image SHA
          │
          ▼
8. Git change committed
          │
          ▼
9. Argo CD detects change
          │
          ▼
10. Kustomize generates manifests
          │
          ▼
11. Kubernetes deployment updated
          │
          ▼
12. New pods start
          │
          ▼
13. Health checks pass
          │
          ▼
14. Traffic moves to new pods
          │
          ▼
15. Old pods are removed
```

---

# 🧪 Testing

Run tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ \
  --cov=app \
  --cov-report=term-missing
```

---

# 🔍 Useful Kubernetes Commands

### View pods

```bash
kubectl get pods -n gitops-demo
```

### View deployments

```bash
kubectl get deployments -n gitops-demo
```

### View services

```bash
kubectl get svc -n gitops-demo
```

### View pod logs

```bash
kubectl logs -n gitops-demo deployment/gitops-demo
```

### Describe deployment

```bash
kubectl describe deployment gitops-demo -n gitops-demo
```

### Describe pod

```bash
kubectl describe pod <pod-name> -n gitops-demo
```

### View events

```bash
kubectl get events -n gitops-demo
```

### Watch pods

```bash
kubectl get pods -n gitops-demo -w
```

---

# 🔙 Rollback

Because the Docker images use Git SHA tags, deployments can be rolled back to a previous image version.

Example:

```text
Current:

sha-a1b2c3d

Previous:

sha-91f4e2a
```

Update the Kustomize image tag to the required SHA and commit the change.

Argo CD will detect the Git change and synchronize Kubernetes.

```text
Git
 ↓
Argo CD
 ↓
Kustomize
 ↓
Kubernetes
 ↓
Previous Version
```

---

# 🧹 Cleanup

The project contains:

```text
scripts/cleanup.sh
```

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

This file is only an example and should not contain real credentials.

For actual deployments, secrets should be managed separately using an appropriate secret-management solution.

---

# 📊 Monitoring Foundation

The application includes basic observability endpoints.

### Health

```text
/health
```

### Readiness

```text
/ready
```

### Metrics

```text
/metrics
```

### Application information

```text
/info
```

### Version information

```text
/version
```

These endpoints provide a foundation for integrating monitoring tools such as Prometheus and Grafana.

---

# 🔮 Possible Extensions

The project can be extended with:

```text
Prometheus
Grafana
Alertmanager
Horizontal Pod Autoscaler
NetworkPolicies
PodDisruptionBudgets
External Secrets
TLS
cert-manager
Argo Rollouts
Canary Deployments
Blue-Green Deployments
Cosign Image Signing
Kyverno
OPA Gatekeeper
Terraform
AWS EKS
```

---

# 🎯 Core Concept

The main concept behind the project is:

```text
                 Git
                  │
                  │ Desired State
                  ▼
               Argo CD
                  │
                  │ Reconciliation
                  ▼
             Kubernetes
                  │
                  │ Actual State
                  └───────────────┐
                                  │
                                  ▼
                           Continuous Sync
```

Instead of manually deploying applications with `kubectl`, the desired Kubernetes configuration is stored in Git and Argo CD continuously keeps the Kubernetes cluster synchronized with that configuration.

---

# 🚀 End-to-End Summary

```text
┌────────────────────────────────────────────────────────┐
│                 GITOPS DEPLOYMENT                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  GitHub                                                │
│     │                                                  │
│     ▼                                                  │
│  GitHub Actions                                        │
│     │                                                  │
│     ├── Tests                                          │
│     ├── Validation                                     │
│     └── Security Scan                                  │
│     │                                                  │
│     ▼                                                  │
│  Docker                                                │
│     │                                                  │
│     ▼                                                  │
│  GHCR                                                  │
│     │                                                  │
│     ▼                                                  │
│  Kustomize                                             │
│     │                                                  │
│     ▼                                                  │
│  Git Configuration                                     │
│     │                                                  │
│     ▼                                                  │
│  Argo CD                                               │
│     │                                                  │
│     ├── Synchronization                                │
│     ├── Self-Healing                                   │
│     └── Pruning                                        │
│     │                                                  │
│     ▼                                                  │
│  Kubernetes                                            │
│     │                                                  │
│     ├── Deployment                                     │
│     ├── Service                                        │
│     ├── ConfigMap                                      │
│     ├── Ingress                                        │
│     └── Pods                                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Git → GitHub Actions → Docker → Trivy → GHCR → Kustomize → GitOps → Argo CD → Kubernetes**
