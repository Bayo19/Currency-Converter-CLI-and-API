import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.db.database_functions import create_tables


@pytest.fixture
def temp_db():
    import os

    temp_db_path = "temp_currencyConverter.db"
    yield temp_db_path
    os.remove(temp_db_path)


@pytest.fixture
def database(temp_db):
    engine = create_engine("sqlite:///temp_currencyConverter.db/", echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    create_tables(eng=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
