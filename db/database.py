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
engine = create_engine(DATABASE_URI, echo=False)
Base = declarative_base()
# creating session
Session = sessionmaker(bind=engine)

