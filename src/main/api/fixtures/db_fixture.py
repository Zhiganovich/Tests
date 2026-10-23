from typing import Generator
from sqlalchemy.orm import Session
import pytest
from src.main.api.db.engine import SessionLocal, engine


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()