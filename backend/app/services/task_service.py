from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskGroupedRead, TaskRead, TaskUpdate


def list_tasks_grouped(db: Session, reference_date: date) -> TaskGroupedRead:
    tasks = (
        db.query(Task)
        .filter(Task.task_date >= reference_date)
        .order_by(Task.task_date, Task.title)
        .all()
    )
    today = [
        TaskRead.model_validate(task)
        for task in tasks
        if task.task_date == reference_date
    ]
    future = [
        TaskRead.model_validate(task)
        for task in tasks
        if task.task_date > reference_date
    ]
    return TaskGroupedRead(today=today, future=future)


def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(title=payload.title, task_date=payload.task_date)
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
