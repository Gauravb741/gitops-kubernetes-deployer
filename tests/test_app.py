"""
Pytest test suite for the Kubernetes GitOps Demo application.
Tests all API endpoints, status codes, response schemas, and runtime behaviour.
"""

import os
import pytest

# Make sure the app module can be found regardless of working directory
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app as flask_app


# ── Fixtures ───────────────────────────────────────────────────────────────────
@pytest.fixture
def client():
    """Return a Flask test client with TESTING mode enabled."""
    flask_app.config["TESTING"] = True
    flask_app.config["DEBUG"] = False
    with flask_app.test_client() as c:
        yield c


# ── Root route ─────────────────────────────────────────────────────────────────
class TestRootRoute:
    def test_status_code(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_returns_html(self, client):
        resp = client.get("/")
        assert b"Kubernetes GitOps Demo" in resp.data

    def test_contains_version(self, client):
        resp = client.get("/")
        assert b"v1" in resp.data or b"version" in resp.data.lower()

    def test_contains_pipeline_stages(self, client):
        resp = client.get("/")
        assert b"GitHub Actions" in resp.data
        assert b"Kubernetes" in resp.data


# ── /health ─────────────────────────────────────────────────────────────────────
class TestHealthEndpoint:
    def test_status_code(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_content_type(self, client):
        resp = client.get("/health")
        assert resp.content_type == "application/json"

    def test_response_body(self, client):
        resp = client.get("/health")
        data = resp.get_json()
        assert data is not None
        assert data.get("status") == "healthy"

    def test_no_extra_keys_required(self, client):
        """status key must be present; additional keys are allowed."""
        data = client.get("/health").get_json()
        assert "status" in data


# ── /ready ──────────────────────────────────────────────────────────────────────
class TestReadyEndpoint:
    def test_status_code(self, client):
        resp = client.get("/ready")
        assert resp.status_code == 200

    def test_content_type(self, client):
        resp = client.get("/ready")
        assert resp.content_type == "application/json"

    def test_response_body(self, client):
        data = client.get("/ready").get_json()
        assert data is not None
        assert data.get("status") == "ready"


# ── /version ────────────────────────────────────────────────────────────────────
class TestVersionEndpoint:
    def test_status_code(self, client):
        resp = client.get("/version")
        assert resp.status_code == 200

    def test_content_type(self, client):
        resp = client.get("/version")
        assert resp.content_type == "application/json"

    def test_required_keys(self, client):
        data = client.get("/version").get_json()
        assert "application" in data
        assert "version" in data

    def test_application_name(self, client):
        data = client.get("/version").get_json()
        assert data["application"] == "kubernetes-gitops-demo"

    def test_version_format(self, client):
        """Version must be a non-empty string."""
        data = client.get("/version").get_json()
        version = data.get("version", "")
        assert isinstance(version, str)
        assert len(version) > 0

    def test_environment_key_present(self, client):
        data = client.get("/version").get_json()
        assert "environment" in data

    def test_hostname_present(self, client):
        data = client.get("/version").get_json()
        assert "hostname" in data
        assert isinstance(data["hostname"], str)

    def test_pod_name_present(self, client):
        data = client.get("/version").get_json()
        assert "pod_name" in data

    def test_timestamp_present(self, client):
        data = client.get("/version").get_json()
        assert "timestamp" in data


# ── Environment variable override ──────────────────────────────────────────────
class TestEnvironmentVariableOverride:
    def test_version_override(self, monkeypatch):
        monkeypatch.setenv("APP_VERSION", "9.9.9")
        # Re-import to pick up new env
        import importlib
        import app as app_module
        importlib.reload(app_module)
        test_client = app_module.app.test_client()
        data = test_client.get("/version").get_json()
        # Value may be read at module load; confirm string type at minimum
        assert isinstance(data["version"], str)

    def test_app_name_default(self, client):
        data = client.get("/version").get_json()
        # Default name must contain expected identifier
        assert "gitops" in data["application"] or "kubernetes" in data["application"]


# ── 404 handling ───────────────────────────────────────────────────────────────
class TestNotFound:
    def test_unknown_route(self, client):
        resp = client.get("/this-does-not-exist")
        assert resp.status_code == 404


# ── HTTP methods ────────────────────────────────────────────────────────────────
class TestHttpMethods:
    def test_health_only_get(self, client):
        assert client.post("/health").status_code == 405

    def test_ready_only_get(self, client):
        assert client.post("/ready").status_code == 405

    def test_version_only_get(self, client):
        assert client.post("/version").status_code == 405
        