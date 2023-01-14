from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base


meta = MetaData()
engine = create_engine("sqlite:///rates.db", echo=False)
Base = declarative_base()
# creating session
Session = sessionmaker(bind=engine)
session = Session()
