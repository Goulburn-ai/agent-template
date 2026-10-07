import importlib
import sys
import types

from fastapi.testclient import TestClient

OK = {"messages": [{"role": "user", "content": "hi"}]}


def load(monkeypatch, **env):
    for k in ("AGENT_SHARED_SECRET", "RATE_LIMIT_PER_MIN", "GEMINI_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    fake = types.ModuleType("google.generativeai")

    class Model:
        def __init__(self, *a, **k):
            pass

        def generate_content(self, prompt):
            return types.SimpleNamespace(text="echo:" + prompt)

    fake.configure = lambda **k: None
    fake.GenerativeModel = Model
    google = types.ModuleType("google")
    google.generativeai = fake
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.generativeai", fake)
    import agent

    importlib.reload(agent)
    return TestClient(agent.app)


def test_happy_path(monkeypatch):
    r = load(monkeypatch, GEMINI_API_KEY="k").post("/chat", json=OK)
    assert r.status_code == 200 and r.json()["response"] == "echo:hi"


def test_list_shaped_content_is_422_not_500(monkeypatch):
    body = {"messages": [{"role": "user", "content": [{"type": "text", "text": "x"}]}]}
    assert load(monkeypatch, GEMINI_API_KEY="k").post("/chat", json=body).status_code == 422


def test_bad_bodies_are_422(monkeypatch):
    c = load(monkeypatch, GEMINI_API_KEY="k")
    assert c.post("/chat", json={"messages": []}).status_code == 422
    assert c.post("/chat", json={}).status_code == 422
    assert c.post("/chat", content=b"nope", headers={"content-type": "application/json"}).status_code == 422


def test_body_size_cap(monkeypatch):
    c = load(monkeypatch, GEMINI_API_KEY="k")
    r = c.post("/chat", content=b"x" * 70_000, headers={"content-type": "application/json"})
    assert r.status_code == 413


def test_content_length_cap(monkeypatch):
    c = load(monkeypatch, GEMINI_API_KEY="k")
    assert c.post("/chat", json={"messages": [{"content": "a" * 8001}]}).status_code == 422


def test_shared_secret(monkeypatch):
    c = load(monkeypatch, GEMINI_API_KEY="k", AGENT_SHARED_SECRET="s3cret-value")
    assert c.post("/chat", json=OK).status_code == 401
    assert c.post("/chat", json=OK, headers={"Authorization": "Bearer wrong"}).status_code == 401
    assert c.post("/chat", json=OK, headers={"Authorization": "Bearer s3cret-value"}).status_code == 200


def test_rate_limit(monkeypatch):
    c = load(monkeypatch, GEMINI_API_KEY="k", RATE_LIMIT_PER_MIN="3")
    assert [c.post("/chat", json=OK).status_code for _ in range(4)] == [200, 200, 200, 429]


def test_missing_provider_key(monkeypatch):
    assert load(monkeypatch).post("/chat", json=OK).status_code == 500
