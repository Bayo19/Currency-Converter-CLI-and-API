from typing import List, Dict, Callable, Any
from sqlalchemy import or_
from db.models import Rate
from db.database import Base, engine, get_db
from common.utilities import CurrencyRate


def create_table() -> None:
    table_obj = [Rate.__table__]
    Base.metadata.create_all(engine(), tables=table_obj)


def add_rates_to_table(
    data: List[CurrencyRate], db: Callable[..., Any] = get_db
) -> None:
    db().add_all([Rate(currency_code=r.code, rate=r.rate) for r in data])
    db().commit()


def get_rates_from_table(
    from_rate: str, to_rate: str, db: Callable[..., Any] = get_db
) -> Dict[str, float]:
    result = (
        db()
        .query(Rate)
        .filter(or_(Rate.currency_code == from_rate, Rate.currency_code == to_rate))
    )

    # if one or both of the given rates (currency code) are not valid (found in the db) raise ValueError
    if len(result.all()) < 2:
        raise ValueError

    return {r.currency_code: r.rate for r in result.all()}


create_table()
