cat > app/app.py << 'PYTHON_EOF'
"""
Kubernetes GitOps Demo Application
Production-quality Flask app demonstrating GitOps deployment patterns.
Improvements: structured JSON logging, metrics counter, build info endpoint,
graceful shutdown handling, environment-aware configuration.
"""

import logging
import os
import signal
import socket
import sys
import time
from datetime import datetime, timezone
from threading import Event

from flask import Flask, Response, jsonify, render_template, request

# ── Structured logging setup ──────────────────────────────────────────────────
class JSONFormatter(logging.Formatter):
    """Outputs log records as single-line JSON for log aggregation tools."""

    def format(self, record: logging.LogRecord) -> str:
        import json
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level":     record.levelname,
            "logger":    record.name,
            "message":   record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def _configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)


_configure_logging()
logger = logging.getLogger("gitops-demo")

# ── Application factory ───────────────────────────────────────────────────────
app = Flask(__name__)

# ── Runtime configuration ─────────────────────────────────────────────────────
APP_NAME      = os.getenv("APP_NAME",      "kubernetes-gitops-demo")
APP_VERSION   = os.getenv("APP_VERSION",   "1.0.0")
APP_ENV       = os.getenv("APP_ENV",       "development")
POD_NAME      = os.getenv("POD_NAME",      "local")
POD_NAMESPACE = os.getenv("POD_NAMESPACE", "default")
BUILD_DATE    = os.getenv("BUILD_DATE",    "unknown")
GIT_COMMIT    = os.getenv("GIT_COMMIT",    "unknown")
HOSTNAME      = socket.gethostname()
START_TIME    = time.time()

# ── Simple in-memory request counter (improves observability) ─────────────────
_request_count: dict[str, int] = {}
_shutdown_event = Event()

# ── Graceful shutdown handler ─────────────────────────────────────────────────
def _handle_sigterm(signum, frame):  # noqa: ARG001
    logger.info("Received SIGTERM — beginning graceful shutdown")
    _shutdown_event.set()

signal.signal(signal.SIGTERM, _handle_sigterm)

# ── Middleware ────────────────────────────────────────────────────────────────
@app.before_request
def _before() -> None:
    request.start_time = time.perf_counter()  # type: ignore[attr-defined]
    path = request.path
    _request_count[path] = _request_count.get(path, 0) + 1


@app.after_request
def _after(response: Response) -> Response:
    duration_ms = (time.perf_counter() - request.start_time) * 1000  # type: ignore[attr-defined]
    logger.info(
        "HTTP request processed",
        extra={} if True else None,
    )
    # Emit a plain structured log line compatible with most log parsers
    import json
    print(json.dumps({
        "timestamp":   datetime.now(timezone.utc).isoformat(),
        "level":       "INFO",
        "method":      request.method,
        "path":        request.path,
        "status":      response.status_code,
        "duration_ms": round(duration_ms, 2),
        "remote_addr": request.remote_addr,
        "version":     APP_VERSION,
    }), flush=True)
    return response


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Render the main dashboard."""
    uptime_seconds = int(time.time() - START_TIME)
    uptime_str = _format_uptime(uptime_seconds)
    context = {
        "app_name":      APP_NAME,
        "version":       APP_VERSION,
        "environment":   APP_ENV,
        "pod_name":      POD_NAME,
        "pod_namespace": POD_NAMESPACE,
        "hostname":      HOSTNAME,
        "git_commit":    GIT_COMMIT,
        "build_date":    BUILD_DATE,
        "uptime":        uptime_str,
        "timestamp":     datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "request_count": sum(_request_count.values()),
    }
    return render_template("index.html", **context)


@app.route("/health")
def health():
    """Kubernetes liveness probe — returns 200 while process is alive."""
    return jsonify({"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}), 200


@app.route("/ready")
def ready():
    """
    Kubernetes readiness probe.
    Returns 503 during graceful shutdown so traffic stops before process exits.
    """
    if _shutdown_event.is_set():
        return jsonify({"status": "shutting_down"}), 503
    return jsonify({"status": "ready", "timestamp": datetime.now(timezone.utc).isoformat()}), 200


@app.route("/version")
def version():
    """Structured version and build information."""
    return jsonify({
        "application":   APP_NAME,
        "version":       APP_VERSION,
        "environment":   APP_ENV,
        "pod_name":      POD_NAME,
        "pod_namespace": POD_NAMESPACE,
        "hostname":      HOSTNAME,
        "git_commit":    GIT_COMMIT,
        "build_date":    BUILD_DATE,
        "uptime_seconds": int(time.time() - START_TIME),
        "timestamp":     datetime.now(timezone.utc).isoformat(),
    }), 200


@app.route("/metrics")
def metrics():
    """
    Lightweight Prometheus-compatible plain-text metrics.
    Improvement over basic demo: exposes request counts per path and uptime.
    """
    uptime = int(time.time() - START_TIME)
    lines = [
        "# HELP app_uptime_seconds Total uptime of the application in seconds",
        "# TYPE app_uptime_seconds gauge",
        f'app_uptime_seconds{{app="{APP_NAME}",version="{APP_VERSION}",env="{APP_ENV}"}} {uptime}',
        "",
        "# HELP app_http_requests_total Total HTTP requests per path",
        "# TYPE app_http_requests_total counter",
    ]
    for path, count in sorted(_request_count.items()):
        lines.append(
            f'app_http_requests_total{{app="{APP_NAME}",path="{path}"}} {count}'
        )
    lines.append("")
    return Response("\n".join(lines), mimetype="text/plain; version=0.0.4")


@app.route("/info")
def info():
    """Extended application and runtime information for debugging."""
    return jsonify({
        "application": {
            "name":        APP_NAME,
            "version":     APP_VERSION,
            "environment": APP_ENV,
            "git_commit":  GIT_COMMIT,
            "build_date":  BUILD_DATE,
        },
        "runtime": {
            "hostname":      HOSTNAME,
            "pod_name":      POD_NAME,
            "pod_namespace": POD_NAMESPACE,
            "python_version": sys.version,
            "uptime_seconds": int(time.time() - START_TIME),
        },
        "requests": {
            "total":    sum(_request_count.values()),
            "by_path":  _request_count,
        },
    }), 200


# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not_found", "path": request.path}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "method_not_allowed", "method": request.method}), 405


@app.errorhandler(500)
def internal_error(e):
    logger.error("Internal server error: %s", str(e))
    return jsonify({"error": "internal_server_error"}), 500


# ── Helpers ───────────────────────────────────────────────────────────────────
def _format_uptime(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    logger.info(
        "Starting %s v%s on port %d (env=%s, commit=%s)",
        APP_NAME, APP_VERSION, port, APP_ENV, GIT_COMMIT,
    )
    app.run(host="0.0.0.0", port=port, debug=False)
PYTHON_EOF