# ╔══════════════════════════════════════════════════════════╗
# ║  Multi-stage Dockerfile — Kubernetes GitOps Demo         ║
# ║  Stage 1: dependency installation (builder)              ║
# ║  Stage 2: minimal runtime image (production)             ║
# ╚══════════════════════════════════════════════════════════╝

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install dependencies into an isolated prefix so we can copy them cleanly
COPY app/requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Security: create non-root user
RUN groupadd --gid 1001 appgroup \
 && useradd  --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ .

# Metadata labels (OCI Image Spec)
LABEL org.opencontainers.image.title="kubernetes-gitops-demo" \
      org.opencontainers.image.description="GitOps demo application for Kubernetes" \
      org.opencontainers.image.source="https://github.com/owner/kubernetes-gitops-deployment" \
      org.opencontainers.image.licenses="MIT"

# Environment defaults (overridden by ConfigMap / env vars at runtime)
ENV APP_NAME="kubernetes-gitops-demo" \
    APP_VERSION="1.0.0" \
    APP_ENV="production" \
    PORT="8080" \
    PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1"

EXPOSE 8080

# Security: switch to non-root user
USER appuser

# Health check (Docker-level, supplementary to Kubernetes probes)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" \
  || exit 1

# Use gunicorn for production serving
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "2", \
     "--threads", "2", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app:app"]