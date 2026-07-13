import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def _load_tasks() -> dict[str, TaskResponse]:
    if not DATA_FILE.exists():
        return {}

    try:
        raw_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}

    tasks: dict[str, TaskResponse] = {}

    for task_id, task_payload in raw_data.items():
        tasks[task_id] = TaskResponse.model_validate(task_payload)

    return tasks


def _save_tasks(tasks: dict[str, TaskResponse]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    DATA_FILE.write_text(
        json.dumps(
            {
                task_id: task.model_dump(mode="json")
                for task_id, task in tasks.items()
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _get_tasks_store() -> dict[str, TaskResponse]:
    if not hasattr(_get_tasks_store, "_cache"):
        _get_tasks_store._cache = _load_tasks()

    return _get_tasks_store._cache


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and persist a new task in the JSON-backed store.

    Args:
        payload: Task creation data used to build the new task record.

    Returns:
        TaskResponse: The stored task including its generated identifier and
            timestamp values.

    Raises:
        None: The function does not raise an explicit exception for the current
            flow.
    """
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())

    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )

    tasks = _get_tasks_store()
    tasks[task_id] = task
    _save_tasks(tasks)

    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
    search: Optional[str] = None,
) -> list[TaskResponse]:
    """Return stored tasks filtered by the supplied query parameters.

    Args:
        status: Optional status filter applied to the task list.
        priority: Optional priority filter applied to the task list.
        overdue: When True, only overdue tasks that are not marked as done are
            included.
        search: Optional text used to match task titles and descriptions.

    Returns:
        list[TaskResponse]: The filtered list of stored tasks.

    Raises:
        None: The function does not raise an explicit exception for the current
            flow.
    """
    tasks = list(_get_tasks_store().values())

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    if overdue is True:
        today = date.today()

        tasks = [
            task
            for task in tasks
            if task.due_date is not None
            and task.due_date < today
            and task.status != TaskStatus.DONE
        ]
    if search:
        search_value = search.lower()

        tasks = [
            task
            for task in tasks
            if search_value in task.title.lower()
            or search_value in task.description.lower()
        ]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Fetch a task from the in-memory store by identifier.

    Args:
        task_id: Unique identifier of the task to return.

    Returns:
        Optional[TaskResponse]: The matching task when found, otherwise None.

    Raises:
        None: The function does not raise an explicit exception for the current
            flow.
    """
    return _get_tasks_store().get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply partial updates to an existing task and persist the result.

    Args:
        task_id: Unique identifier of the task to update.
        payload: Partial task fields to apply to the stored task.

    Returns:
        Optional[TaskResponse]: The updated task when the identifier exists,
            otherwise None.

    Raises:
        None: The function does not raise an explicit exception for the current
            flow.
    """
    tasks = _get_tasks_store()
    task = tasks.get(task_id)

    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        return task

    updated_task = task.model_copy(
        update={
            **updates,
            "updated_at": datetime.now(timezone.utc),
        }
    )

    tasks[task_id] = updated_task
    _save_tasks(tasks)

    return updated_task


def delete_task(task_id: str) -> bool:
    """Remove a task from the store when it exists.

    Args:
        task_id: Unique identifier of the task to delete.

    Returns:
        bool: True when the task was deleted, otherwise False.

    Raises:
        None: The function does not raise an explicit exception for the current
            flow.
    """
    tasks = _get_tasks_store()

    if task_id not in tasks:
        return False

    del tasks[task_id]
    _save_tasks(tasks)

    return True


def _reset() -> None:
    DATA_FILE.write_text("{}", encoding="utf-8")

    if hasattr(_get_tasks_store, "_cache"):
        _get_tasks_store._cache = {}