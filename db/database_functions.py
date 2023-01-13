from typing import List
from sqlalchemy import or_
from db.models import Rate
from db.database import Base, engine, session as _session
from src.utilities import CurrencyRate


def create_table() -> None:
    table_obj = [Rate.__table__]
    Base.metadata.create_all(engine, tables=table_obj)


def add_rates_to_table(data: List[CurrencyRate], session=_session) -> None:
    session.add_all([Rate(currencyCode=r.code, rate=r.rate) for r in data])
    session.commit()


def get_rates_from_table(from_rate: str, to_rate: str, session=_session) -> dict:
    result = session.query(Rate).filter(
        or_(Rate.currencyCode == from_rate, Rate.currencyCode == to_rate)
    )
    return {r.currencyCode: r.rate for r in result.all()}
