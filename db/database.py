import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
import db.connection_details


USERNAME = os.environ["DB_USERNAME"]
PASSWORD = os.environ["DB_PASSWORD"]
IP_ADDRESS = os.environ["IP_ADDRESS"]
PORT = os.environ["PORT"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DB_NAME}"
meta = MetaData()
Base = declarative_base()

def run_once(func):
    def inner(*args, **kwargs):
        if not inner.has_run:
            result = func(*args, **kwargs)
            inner.has_run = True
            return result
    inner.has_run = False
    return inner

@run_once
def engine():
    engine = create_engine(DATABASE_URI, echo=True)
    return engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine())

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()





