from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

app = FastAPI(
    title="Module 1 Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)

# Only allow the local frontend origins used during development.
# Replace or extend this list if your frontend runs on a different localhost port.
frontend_origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Return a simple health payload for the API service.

    Args:
        None.

    Returns:
        dict[str, str]: A JSON-compatible payload containing the service status and
            the current UTC timestamp.

    Raises:
        None: This endpoint always returns a successful response body.

    Examples:
        Request:
            GET /health
        Response:
            {"status": "ok", "timestamp": "2026-07-11T12:34:56.789012+00:00"}
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task from a request payload.

    Args:
        payload: Task creation data supplied by the client.

    Returns:
        TaskResponse: The created task, including its generated identifier and
            timestamp values.

    Raises:
        None: The handler itself does not raise an explicit exception for a
            successful request. FastAPI/Pydantic may reject invalid input before
            this function runs. [VERIFY]

    Examples:
        Request:
            POST /tasks
            {"title": "Write report", "description": "Draft the weekly summary"}
        Response:
            {"id": "8f4c...", "title": "Write report", "description": "Draft the weekly summary", "status": "ToDo", "priority": "Medium", "assignee": null, "due_date": null, "created_at": "...", "updated_at": "..."}
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
    search: str | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status, priority, overdue state, or search text.

    Args:
        status: Optional task status filter.
        priority: Optional task priority filter.
        overdue: When set to True, only tasks that are overdue and not marked as
            done are returned.
        search: Optional text used to match against task titles and descriptions.

    Returns:
        list[TaskResponse]: A list of matching tasks.

    Raises:
        None: This handler does not raise an explicit exception for successful
            requests.

    Examples:
        Request:
            GET /tasks?status=InProgress&priority=High&overdue=true&search=report
        Response:
            [{"id": "...", "title": "Write report", "description": "...", "status": "InProgress", "priority": "High", "assignee": null, "due_date": "...", "created_at": "...", "updated_at": "..."}]
    """
    return storage.get_all_tasks(
        status=status,
        priority=priority,
        overdue=overdue,
        search=search,
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by its identifier.

    Args:
        task_id: Unique identifier of the task to fetch.

    Returns:
        TaskResponse: The stored task matching the provided identifier.

    Raises:
        HTTPException: Raised with status code 404 if no task exists for the
            supplied identifier.

    Examples:
        Request:
            GET /tasks/123
        Response:
            {"id": "123", "title": "Write report", "description": "...", "status": "ToDo", "priority": "Medium", "assignee": null, "due_date": null, "created_at": "...", "updated_at": "..."}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Update an existing task with partial changes.

    Args:
        task_id: Unique identifier of the task to update.
        payload: Partial task fields to replace on the stored task.

    Returns:
        TaskResponse: The updated task after applying the supplied changes.

    Raises:
        HTTPException: Raised with status code 404 if no task exists for the
            supplied identifier, or with status code 422 if a status transition
            is invalid.

    Examples:
        Request:
            PATCH /tasks/123
            {"status": "InProgress"}
        Response:
            {"id": "123", "title": "Write report", "description": "...", "status": "InProgress", "priority": "Medium", "assignee": null, "due_date": null, "created_at": "...", "updated_at": "..."}
    """
    if payload.status is not None:
        existing_task = storage.get_task_by_id(task_id)
        if existing_task is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing_task.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str):
    if storage.delete_task(task_id):
        return None
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")