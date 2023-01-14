from typing import List, Dict
from sqlalchemy import or_
from db.models import Rate
from db.database import Base, engine, Session
from src.utilities import CurrencyRate


def create_table() -> None:
    table_obj = [Rate.__table__]
    Base.metadata.create_all(engine, tables=table_obj)


def add_rates_to_table(data: List[CurrencyRate], session=Session()) -> None:
    session.add_all([Rate(currencyCode=r.code, rate=r.rate) for r in data])
    session.commit()


def get_rates_from_table(from_rate: str, to_rate: str, session=Session()) -> Dict[str, float]:
    result = session.query(Rate).filter(
        or_(Rate.currencyCode == from_rate, Rate.currencyCode == to_rate)
    )
    return {r.currencyCode: r.rate for r in result.all()}
