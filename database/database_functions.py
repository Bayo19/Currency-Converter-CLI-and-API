from ..command_functions import ingest_rates
from models import Rate
from database import Base, engine, session as _session
from typing import List


# def create_table():
#     # Create Table
#     table_obj = [Rate.__table__]
#     Base.metadata.create_all(engine, tables=table_obj)


# def add_rates_to_table(data: List[CurrencyRate], session=_session):
#     # Adding object to table?

#     session.add_all(Rate(currencyCode="GBP", rate=0.344))
#     session.commit()


