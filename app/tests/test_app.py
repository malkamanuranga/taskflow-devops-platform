import pytest

import app as app_module

@pytest.fixture
def client():
    app_module.tasks.clear()
    app_module.next_id = 1
    return app_module.app.test_client()

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_create_task(client):
    res = client.post("/tasks", json={"title": "learn docker"})
    assert res.status_code == 201
    assert res.get_json()["title"] == "learn docker"

def test_create_task_requires_title(client):
    res = client.post("/tasks", json={})
    assert res.status_code == 400




def test_get_missing_task(client):
    assert client.get("/tasks/99").status_code == 404


def test_mark_done(client):
    client.post("/tasks", json={"title": "write pipeline"})
    res = client.post("/tasks/1/done")
    assert res.get_json()["done"] is True


def test_delete_task(client):
    client.post("/tasks", json={"title": "cleanup"})
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks/1").status_code == 404
