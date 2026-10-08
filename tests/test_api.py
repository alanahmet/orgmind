import os

os.environ["ORGMIND_DB"] = ":memory:"

from fastapi.testclient import TestClient  # noqa: E402

from orgmind import llm  # noqa: E402
from orgmind.api import app  # noqa: E402

client = TestClient(app)


def test_permissions_ask_and_analytics(monkeypatch):
    monkeypatch.setattr(llm, "complete", lambda system, prompt, **kw: "ok")
    hr = client.post("/departments", json={"name": "HR"}).json()["id"]
    eng = client.post("/departments", json={"name": "Engineering"}).json()["id"]
    admin = client.post("/users", json={"name": "A", "email": "a@x", "role": "admin"}).json()["id"]
    dev = client.post("/users", json={"name": "D", "email": "d@x", "department_id": eng}).json()["id"]

    client.post("/documents", headers={"X-User-Id": str(admin)},
                json={"title": "Salary bands", "content": "salary bands secret", "department_id": hr})
    client.post("/documents", headers={"X-User-Id": str(admin)},
                json={"title": "Leave policy", "content": "salary paid during leave"})

    r = client.post("/ask", headers={"X-User-Id": str(dev)}, json={"question": "salary"}).json()
    assert [s["title"] for s in r["sources"]] == ["Leave policy"]

    assert client.get("/analytics", headers={"X-User-Id": str(dev)}).status_code == 403
    stats = client.get("/analytics", headers={"X-User-Id": str(admin)}).json()
    assert {"name": "Engineering", "ai_actions": 1, "open_tasks": 0} in stats
