"""
Shared pytest fixtures for the backend test suite.

Provides an isolated in-memory SQLite database per test, a FastAPI
TestClient wired to that database, and reusable fixtures so tests
never touch the real database file or make real network calls.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="function", autouse=True)
def setup_database(tmp_path):
    """Create all tables before each test and drop them afterward for isolation."""
    Base.metadata.create_all(bind=engine)
    settings.history_storage_dir = str(tmp_path)
    storage_dir = Path(settings.history_storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)
    for file_path in storage_dir.glob("*.json"):
        file_path.unlink(missing_ok=True)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """Provide a database session for direct service/repository-level tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def _override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client():
    """Provide a FastAPI TestClient wired to the isolated test database."""
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
