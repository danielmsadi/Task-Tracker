import importlib

from fastapi.testclient import TestClient

from app import storage
from app.main import app
from app.models import TaskCreate

client = TestClient(app)


def setup_function():
    storage._reset()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Write docs",
            "description": "Document the API",
            "status": "ToDo",
            "priority": "High",
            "assignee": "Dana",
        },
    )

    assert create_response.status_code == 201
    payload = create_response.json()
    assert payload["title"] == "Write docs"
    assert payload["id"]

    task_id = payload["id"]
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id


def test_list_tasks_filters_and_returns_collection():
    client.post("/tasks", json={"title": "First", "status": "ToDo", "priority": "Low"})
    client.post("/tasks", json={"title": "Second", "status": "InProgress", "priority": "High"})

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2

    filtered = client.get("/tasks", params={"status": "ToDo"})
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1
    assert filtered.json()[0]["title"] == "First"


def test_update_task():
    create_response = client.post("/tasks", json={"title": "Old title"})
    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "New title", "status": "InProgress"},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "New title"
    assert updated["status"] == "InProgress"


def test_update_task_rejects_invalid_status_transition():
    create_response = client.post("/tasks", json={"title": "Start task", "status": "ToDo"})
    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "Done"},
    )

    assert update_response.status_code == 422
    assert "Invalid status transition" in update_response.json()["detail"]


def test_delete_task_and_missing_task_returns_404():
    create_response = client.post("/tasks", json={"title": "Delete me"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/tasks/{task_id}")
    assert missing_response.status_code == 404


def test_tasks_persist_after_module_reload():
    created_task = storage.add_task(TaskCreate(title="Persisted task"))

    import app.storage as storage_module

    reloaded_module = importlib.reload(storage_module)
    reloaded_task = reloaded_module.get_task_by_id(created_task.id)

    assert reloaded_task is not None
    assert reloaded_task.title == "Persisted task"
