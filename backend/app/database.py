from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BACKEND_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BACKEND_ROOT / "app.db"
DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import task  # noqa: F401

    Base.metadata.create_all(bind=engine)
