from typing import Callable, Any
from datetime import datetime
from time import sleep
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.models import Rate, Portfolio, PortfolioBalance
from db.database import Base, engine, get_db
from common.data_types import CurrencyRate


def create_tables() -> None:
    table_obj = [Rate.__table__, Portfolio.__table__, PortfolioBalance.__table__]
    Base.metadata.create_all(engine(), tables=table_obj)


def add_rates_to_table(
    data: list[CurrencyRate], db: Callable[..., Any] = get_db
) -> None:
    db().add_all([Rate(currency_code=r.code, rate=r.rate) for r in data])
    db().commit()


def get_rates_from_table(
    from_rate: str, to_rate: str, db: Callable[..., Session] = get_db
) -> dict[str, float]:
    """
    Retrieves exchanges rates from database table
    """
    db: Session = db()
    result = db.query(Rate).filter(
        or_(Rate.currency_code == from_rate, Rate.currency_code == to_rate)
    )

    # if one or both of the given rates (currency code) are not valid (found in the db) raise ValueError
    if len(result.all()) < 2:
        raise ValueError

    return {r.currency_code: r.rate for r in result.all()}


def get_portfolio_from_table(username: str) -> dict:
    ...


def create_new_portfolio_user(
    username: str, db: Callable[..., Session] = get_db
) -> None:
    db: Session = db()
    portfolio_post = Portfolio(username=username)
    db.add(portfolio_post)
    db.commit()


def add_balances_to_portfolio_balance_table(
    username: str, currencies: dict[str, float], db: Callable[..., Session] = get_db
) -> None:
    """
    Adds new data to portfolio_balance table with given currencies
    and updates balances if they already exist for given user
    """
    db: Session = db()
    portfolio_id = db.query(Portfolio.id).filter_by(username=username)
    timestamp = datetime.now()

    for currency, amount in currencies.items():

        balance: PortfolioBalance = (
            db.query(PortfolioBalance)
            .filter_by(portfolio_id=portfolio_id, currency=currency)
            .one_or_none()
        )

        if balance:
            balance.amount += amount
        else:
            balance = PortfolioBalance(
                currency=currency,
                amount=amount,
                timestamp=timestamp,
                portfolio_id=portfolio_id,
            )
            db.add(balance)
            sleep(0.3)

    db.commit()


create_tables()
