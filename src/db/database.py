from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from src.db.connection_details import USERNAME, PASSWORD, IP_ADDRESS, PORT, DB_NAME

DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DB_NAME}"
meta = MetaData()
Base = declarative_base()


def engine():
    return create_engine(DATABASE_URI, echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine())


def get_db():
    _db = SessionLocal()
    try:
        return _db
    finally:
        _db.close()
