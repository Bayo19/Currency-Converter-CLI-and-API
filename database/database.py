from sqlalchemy import create_engine, Column, String, Float, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

meta = MetaData()
# Engine 
engine = create_engine('sqlite:///rates.db', echo = True)

Base = declarative_base()

# creating session
Session = sessionmaker(bind=engine)
session = Session()




# purge table
# session.query(Rate).delete()
# session.commit()