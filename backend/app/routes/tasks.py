from datetime import date

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(
    date: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
):
    return task_service.list_tasks_for_date(db, date)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, payload)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)
):
    return task_service.update_task(db, task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete_task(db, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
