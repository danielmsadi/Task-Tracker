from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    # Stay in same status (allow editing without changing status)
    (TaskStatus.TODO, TaskStatus.TODO),
    (TaskStatus.IN_PROGRESS, TaskStatus.IN_PROGRESS),
    (TaskStatus.DONE, TaskStatus.DONE),
    # Forward transitions
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Validate whether a requested task status transition is allowed.

    Args:
        current: The task's current status.
        new: The requested status value for the task.

    Returns:
        None: The function returns normally when the transition is allowed.

    Raises:
        HTTPException: Raised with status code 422 when the transition is not
            permitted.
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{from_status.value}->{to_status.value}" for from_status, to_status in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
