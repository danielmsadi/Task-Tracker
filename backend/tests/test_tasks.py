def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Write docs",
            "description": "Document the API",
            "status": "ToDo",
            "priority": "High",
            "assignee": "Dana",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write docs"
    assert body["description"] == "Document the API"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "Dana"
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={"description": "missing title"})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Invalid priority", "priority": "Critical"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Bad field", "unknown": "value"})

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "First", "status": "ToDo"})

    response = client.get("/tasks", params={"status": "Done"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})

    response = client.get("/tasks", params={"priority": "Low"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Low task"
    assert body[0]["priority"] == "Low"


def test_get_task_by_id_returns_task(client, created_task):
    task_id = created_task["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == task_id
    assert body["title"] == "fixture task"


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/does-not-exist")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_patch_partial_update_keeps_other_fields(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Original",
            "description": "Keep me",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": "Dana",
        },
    )
    task_id = response.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"title": "Updated"})

    assert patch_response.status_code == 200
    body = patch_response.json()
    assert body["title"] == "Updated"
    assert body["description"] == "Keep me"
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["assignee"] == "Dana"


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/does-not-exist", json={"title": "Nope"})

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_patch_valid_transition_todo_to_inprogress_returns_200(client):
    response = client.post("/tasks", json={"title": "Start task", "status": "ToDo"})
    task_id = response.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client):
    response = client.post("/tasks", json={"title": "Bad transition", "status": "ToDo"})
    task_id = response.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})

    assert patch_response.status_code == 422


def test_patch_same_status_returns_422(client):
    response = client.post("/tasks", json={"title": "Same status", "status": "ToDo"})
    task_id = response.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})

    assert patch_response.status_code == 422


def test_patch_inprogress_to_done_returns_200_and_done_status(client):
    response = client.post("/tasks", json={"title": "Finish task", "status": "InProgress"})
    task_id = response.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "Done"


def test_delete_existing_returns_204_no_body(client):
    response = client.post("/tasks", json={"title": "Delete me"})
    task_id = response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/does-not-exist")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
