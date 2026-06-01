from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def _sort_key(task: Task) -> tuple:
    if task.due_time is not None:
        return (0, task.due_time, "")
    return (1, task.due_time, task.title.lower())


def list_tasks_for_date(db: Session, task_date: date) -> list[Task]:
    tasks = db.query(Task).filter(Task.task_date == task_date).all()
    return sorted(tasks, key=_sort_key)


def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(
        title=payload.title,
        task_date=payload.task_date,
        due_time=payload.due_time,
        is_done=False,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, payload: TaskUpdate) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
