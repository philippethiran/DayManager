from datetime import date, datetime, time
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    task_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    due_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
