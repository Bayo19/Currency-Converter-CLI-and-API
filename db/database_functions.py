from typing import Callable, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.models import Rate, Portfolio, PortfolioBalance
from db.database import Base, engine, get_db
from common.data_types import CurrencyRate, PortfolioItem


def create_tables() -> None:
    table_obj = [Rate.__table__, Portfolio.__table__, PortfolioBalance.__table__]
    Base.metadata.create_all(engine(), tables=table_obj)


def add_rates_to_table(
    data: list[CurrencyRate], db: Callable[..., Any] = get_db
) -> None:
    db: Session = db()
    db.add_all([Rate(currency_code=r.code, rate=r.rate) for r in data])
    db.commit()


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
    if from_rate != to_rate and len(result.all()) < 2:
        raise ValueError

    return {r.currency_code: r.rate for r in result.all()}


def get_portfolio_from_table(username: str, db: Callable[..., Session] = get_db) -> list[PortfolioItem]:
    db: Session = db()
    portfolio = db.query(Portfolio.username, Portfolio.id, PortfolioBalance.currency, PortfolioBalance.amount, PortfolioBalance.timestamp).filter(Portfolio.id == PortfolioBalance.portfolio_id).filter_by(username=username).all()
    return [PortfolioItem(*p) for p in portfolio]

def user_exists(username: str, db: Callable[..., Session] = get_db) -> bool:
    db: Session = db()
    if db.query(Portfolio.username).filter_by(username=username).one_or_none():
        return True
    return False


def create_new_portfolio_user(
    username: str, db: Callable[..., Session] = get_db
) -> None:
    db: Session = db()

    if not user_exists(username=username):
        portfolio_post = Portfolio(username=username)
        db.add(portfolio_post)
        db.commit()
    else:
        raise ValueError


def add_amount_to_currency(
    username: str, currency: str, amount: float, db: Callable[..., Session] = get_db
):
    """
    Add amount to currency for user if currency exist else create currency in portfolio for user with value of amount
    """
    db: Session = db()
    portfolio_id = db.query(Portfolio.id).filter_by(username=username)
    balance: PortfolioBalance = (
        db.query(PortfolioBalance)
        .filter_by(portfolio_id=portfolio_id, currency=currency)
        .one_or_none()
    )
    timestamp = datetime.now()

    if balance:
        balance.amount += amount
        db.add(balance)
    else:
        balance = PortfolioBalance(
            currency=currency,
            amount=amount,
            timestamp=timestamp,
            portfolio_id=portfolio_id,
        )
    db.commit()


def subtract_amount_from_currency(
    username: str, currency: str, amount: float, db: Callable[..., Session] = get_db
):

    """
    Subtract amount from currency for user
    """
    db: Session = db()
    portfolio_id = db.query(Portfolio.id).filter_by(username=username)
    balance: PortfolioBalance = (
        db.query(PortfolioBalance)
        .filter_by(portfolio_id=portfolio_id, currency=currency)
        .one_or_none()
    )
    if balance:
        balance.amount -= amount
        db.add(balance)
        db.commit()
    else:
        raise ValueError


def add_balances_to_portfolio_balance_table(
    username: str, balance_map: dict[str, float]
) -> None:
    """
    Adds new data to portfolio_balance table with given currencies
    and updates balances if they already exist for given user
    """

    for currency, amount in balance_map.items():
        add_amount_to_currency(username=username, currency=currency, amount=amount)



create_tables()
