import logging
import os
import socket
import sys
from datetime import datetime, timezone

from flask import Flask, jsonify, request, Response

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("gitops-demo")

# ── Application ───────────────────────────────────────────────
app = Flask(__name__)

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


def _render_index() -> str:
    """Return the dashboard HTML as a string — no external template file needed."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kubernetes GitOps Demo</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #0d1117; --surface: #161b22; --surface2: #21262d;
      --border: #30363d; --text: #e6edf3; --text-muted: #8b949e;
      --accent: #58a6ff; --accent2: #3fb950; --warning: #d29922;
      --radius: 12px; --shadow: 0 4px 24px rgba(0,0,0,0.4);
    }}
    body {{
      background: var(--bg); color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh; line-height: 1.6;
    }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .header {{ margin-bottom: 2rem; }}
    .header-inner {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 1.25rem 1.5rem; background: var(--surface);
      border: 1px solid var(--border); border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}
    .logo {{ display: flex; align-items: center; gap: 0.6rem; }}
    .logo-k8s {{ font-size: 1.8rem; color: var(--accent); }}
    .logo-text {{ font-size: 1.25rem; font-weight: 700; }}
    .status-badge {{
      display: flex; align-items: center; gap: 0.4rem;
      padding: 0.35rem 0.85rem; background: rgba(63,185,80,0.15);
      border: 1px solid rgba(63,185,80,0.4); border-radius: 999px;
    }}
    .status-dot {{
      width: 8px; height: 8px; background: var(--accent2);
      border-radius: 50%; animation: pulse 2s ease-in-out infinite;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.6; transform: scale(0.85); }}
    }}
    .status-text {{ font-size: 0.85rem; font-weight: 600; color: var(--accent2); }}
    .card {{
      background: var(--surface); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 1.5rem;
      margin-bottom: 1.25rem; box-shadow: var(--shadow);
    }}
    .card-title {{
      font-size: 0.9rem; font-weight: 600; color: var(--text-muted);
      text-transform: uppercase; letter-spacing: 0.06em;
      margin-bottom: 1.25rem; padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--border);
    }}
    .info-grid {{ display: grid; gap: 0.85rem; }}
    .info-item {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 0.65rem 1rem; background: var(--surface2);
      border: 1px solid var(--border); border-radius: 8px;
    }}
    .info-label {{ font-size: 0.875rem; color: var(--text-muted); font-weight: 500; }}
    .info-value {{ font-size: 0.875rem; color: var(--text); font-weight: 600; }}
    .mono {{
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 0.82rem; color: var(--accent);
    }}
    .version-badge {{
      background: rgba(88,166,255,0.15); border: 1px solid rgba(88,166,255,0.4);
      border-radius: 6px; padding: 0.2rem 0.6rem; color: var(--accent);
    }}
    .env-badge {{
      background: rgba(210,153,34,0.15); border: 1px solid rgba(210,153,34,0.4);
      border-radius: 6px; padding: 0.2rem 0.6rem; color: var(--warning);
      text-transform: uppercase; font-size: 0.78rem;
    }}
    .pipeline {{
      display: flex; align-items: center; flex-wrap: wrap; gap: 0.4rem;
    }}
    .pipeline-step {{
      display: flex; flex-direction: column; align-items: center;
      gap: 0.4rem; padding: 0.75rem 1rem; background: var(--surface2);
      border: 1px solid var(--border); border-radius: 10px;
      flex: 1; min-width: 80px; transition: border-color 0.2s;
    }}
    .pipeline-step:hover {{ border-color: var(--accent); }}
    .step-icon {{ font-size: 1.4rem; }}
    .step-label {{
      font-size: 0.72rem; color: var(--text-muted);
      font-weight: 600; text-align: center;
    }}
    .pipeline-arrow {{
      color: var(--accent); font-size: 1.2rem;
      font-weight: 700; flex-shrink: 0;
    }}
    .endpoints {{ display: flex; flex-direction: column; gap: 0.6rem; }}
    .endpoint-link {{
      display: flex; align-items: center; gap: 0.85rem;
      padding: 0.75rem 1rem; background: var(--surface2);
      border: 1px solid var(--border); border-radius: 8px;
      text-decoration: none; transition: border-color 0.2s;
    }}
    .endpoint-link:hover {{ border-color: var(--accent); }}
    .endpoint-method {{
      font-family: monospace; font-size: 0.75rem; font-weight: 700;
      color: var(--accent2); background: rgba(63,185,80,0.15);
      border: 1px solid rgba(63,185,80,0.3); border-radius: 4px;
      padding: 0.15rem 0.5rem; min-width: 40px; text-align: center;
    }}
    .endpoint-path {{
      font-family: monospace; font-size: 0.875rem;
      color: var(--accent); font-weight: 600;
    }}
    .endpoint-desc {{ font-size: 0.8rem; color: var(--text-muted); margin-left: auto; }}
    .footer {{
      text-align: center; padding: 1.5rem 0 0.5rem;
      font-size: 0.8rem; color: var(--text-muted);
    }}
    @media (max-width: 600px) {{
      .header-inner {{ flex-direction: column; gap: 1rem; }}
      .pipeline-arrow {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-k8s">&#9096;</span>
          <span class="logo-text">Kubernetes GitOps Demo</span>
        </div>
        <div class="status-badge">
          <span class="status-dot"></span>
          <span class="status-text">Running</span>
        </div>
      </div>
    </header>
    <main>
      <section class="card">
        <h2 class="card-title">Runtime Information</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Application Version</span>
            <span class="info-value version-badge">v{APP_VERSION}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Environment</span>
            <span class="info-value env-badge">{APP_ENV}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Pod Name</span>
            <span class="info-value mono">{POD_NAME}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Hostname</span>
            <span class="info-value mono">{HOSTNAME}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Timestamp (UTC)</span>
            <span class="info-value mono">{timestamp}</span>
          </div>
        </div>
      </section>
      <section class="card">
        <h2 class="card-title">Deployment Pipeline</h2>
        <div class="pipeline">
          <div class="pipeline-step">
            <div class="step-icon">&#128104;&#8205;&#128187;</div>
            <div class="step-label">Developer</div>
          </div>
          <div class="pipeline-arrow">&#8594;</div>
          <div class="pipeline-step">
            <div class="step-icon">&#128025;</div>
            <div class="step-label">GitHub</div>
          </div>
          <div class="pipeline-arrow">&#8594;</div>
          <div class="pipeline-step">
            <div class="step-icon">&#9881;</div>
            <div class="step-label">GitHub Actions</div>
          </div>
          <div class="pipeline-arrow">&#8594;</div>
          <div class="pipeline-step">
            <div class="step-icon">&#128051;</div>
            <div class="step-label">Docker / GHCR</div>
          </div>
          <div class="pipeline-arrow">&#8594;</div>
          <div class="pipeline-step">
            <div class="step-icon">&#128260;</div>
            <div class="step-label">Argo CD</div>
          </div>
          <div class="pipeline-arrow">&#8594;</div>
          <div class="pipeline-step">
            <div class="step-icon">&#9096;</div>
            <div class="step-label">Kubernetes</div>
          </div>
        </div>
      </section>
      <section class="card">
        <h2 class="card-title">Health Endpoints</h2>
        <div class="endpoints">
          <a class="endpoint-link" href="/health" target="_blank">
            <span class="endpoint-method">GET</span>
            <span class="endpoint-path">/health</span>
            <span class="endpoint-desc">Liveness probe</span>
          </a>
          <a class="endpoint-link" href="/ready" target="_blank">
            <span class="endpoint-method">GET</span>
            <span class="endpoint-path">/ready</span>
            <span class="endpoint-desc">Readiness probe</span>
          </a>
          <a class="endpoint-link" href="/version" target="_blank">
            <span class="endpoint-method">GET</span>
            <span class="endpoint-path">/version</span>
            <span class="endpoint-desc">Version info</span>
          </a>
        </div>
      </section>
    </main>
    <footer class="footer">
      <p>{APP_NAME} &bull; GitOps with Argo CD &bull; Kubernetes</p>
    </footer>
  </div>
</body>
</html>"""


# ── Routes ────────────────────────────────────────────────────
@app.route("/")
def index():
    return Response(_render_index(), status=200, mimetype="text/html")


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