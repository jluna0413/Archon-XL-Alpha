import sys
import pathlib

# Ensure `src` is on sys.path so imports work when pytest runs from repo root
repo_root = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / "src"))

from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "ok"
    assert body.get("service") == "archon-core"
