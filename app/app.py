import logging
import os
import socket
import sys
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("gitops-demo")

# ── Resolve paths relative to this file ───────────────────────
# This ensures templates and static files are found correctly
# whether the app is run directly, via gunicorn, or via pytest
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ── Application ───────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)

# ── Runtime configuration ─────────────────────────────────────
APP_NAME = os.getenv("APP_NAME", "kubernetes-gitops-demo")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "development")
POD_NAME = os.getenv("POD_NAME", "local")
HOSTNAME = socket.gethostname()


# ── Request logging ───────────────────────────────────────────
@app.before_request
def log_request():
    logger.info(
        "REQUEST method=%s path=%s remote=%s",
        request.method,
        request.path,
        request.remote_addr,
    )


@app.after_request
def log_response(response):
    logger.info(
        "RESPONSE status=%s path=%s version=%s",
        response.status_code,
        request.path,
        APP_VERSION,
    )
    return response


# ── Routes ────────────────────────────────────────────────────
@app.route("/")
def index():
    context = {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "pod_name": POD_NAME,
        "hostname": HOSTNAME,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    return render_template("index.html", **context)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200


@app.route("/version")
def version():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "pod_name": POD_NAME,
        "hostname": HOSTNAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200


# ── Entrypoint ────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    logger.info(
        "Starting %s v%s on port %d (env=%s)",
        APP_NAME, APP_VERSION, port, APP_ENV
    )
    app.run(host="0.0.0.0", port=port, debug=False)