"""
Database configuration module.

Provides the SQLAlchemy engine, session factory, declarative base,
and a FastAPI dependency for obtaining request-scoped DB sessions.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)


class Base(DeclarativeBase):
    """Declarative base class for all SQLAlchemy ORM models."""

    pass


def init_db() -> None:
    """
    Create all database tables registered on the Base metadata.

    Should be called once at application startup. Safe to call
    repeatedly — existing tables are left untouched.

    Returns:
        None
    """
    from app.models import pull_request, review  # noqa: F401 (ensures models are registered)

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a request-scoped SQLAlchemy session.

    Ensures the session is always closed after the request completes,
    even if an exception is raised.

    Yields:
        Session: An active SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()