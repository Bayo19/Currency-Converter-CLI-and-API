from typing import Callable, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.models import Rate, Portfolio, PortfolioBalance
from db.database import Base, engine, get_db
from common.data_types import CurrencyRate, PortfolioItem


def create_tables(eng=engine()) -> None:
    """Create database tables."""
    table_obj = [Rate.__table__, Portfolio.__table__, PortfolioBalance.__table__]
    Base.metadata.create_all(eng, tables=table_obj)


def add_rates_to_table(
    data: list[CurrencyRate], db: Callable[..., Any] = get_db()
) -> None:
    """
    Add currency rates to the database.

    Args:
        data: A list of `CurrencyRate` objects.
        db: A function that returns a `Session` object.
    """
    db.add_all([Rate(currency_code=r.code, rate=r.rate) for r in data])
    db.commit()


def get_rates_from_table(
    from_rate: str, to_rate: str, db: Callable[..., Session] = get_db()
) -> dict[str, float]:
    """
    Retrieve exchange rates from the database.

    Args:
        from_rate: The currency code to convert from.
        to_rate: The currency code to convert to.
        db: A function that returns a `Session` object.

    Returns:
        A dictionary containing the exchange rates.
    """
    result = db.query(Rate).filter(
        or_(Rate.currency_code == from_rate, Rate.currency_code == to_rate)
    )

    # if one or both of the given rates (currency code) are not valid (found in the db) raise ValueError
    if from_rate != to_rate and len(result.all()) < 2:
        raise ValueError

    return {r.currency_code: r.rate for r in result.all()}


def get_portfolio_from_table(
    username: str, db: Callable[..., Session] = get_db()
) -> list[PortfolioItem]:

    """
    Retrieve the portfolio for a user.

    Args:
        username: The username.
        db: A function that returns a `Session` object.

    Returns:
        A list of `PortfolioItem` objects.
    """
    portfolio = (
        db.query(
            Portfolio.username,
            Portfolio.id,
            PortfolioBalance.currency,
            PortfolioBalance.amount,
            PortfolioBalance.timestamp,
        )
        .filter(Portfolio.id == PortfolioBalance.portfolio_id)
        .filter_by(username=username)
        .all()
    )
    return [PortfolioItem(*p) for p in portfolio]


def user_exists(username: str, db: Callable[..., Session] = get_db()) -> bool:
    """
    Check if user exists.

    Args:
        username: The username.
        db: A function that returns a `Session` object.

    Returns:
        True if user exists else False
    """
    return bool(db.query(Portfolio.username).filter_by(username=username).one_or_none())


def create_new_portfolio_user(
    username: str, db: Callable[..., Session] = get_db()
) -> bool:

    """
    Creates new portfolio user if name does not exist in database

    Args:
        username: The username.
        db: A function that returns a `Session` object.

    Returns:
        True if user did not exist else False
    """
    if not user_exists(username=username):
        portfolio_post = Portfolio(username=username)
        db.add(portfolio_post)
        db.commit()
        return True
    return False


def add_amount_to_currency(
    username: str, currency: str, amount: float, db: Callable[..., Session] = get_db()
) -> None:
    """
    Add amount to currency for user if currency exists else
    create currency in portfolio for user with value of amount

    Args:
        username: The username.
        currency: The currency code of money being added.
        amount: The amount of money being added.
        db: A function that returns a `Session` object.
    """
    portfolio_id = db.query(Portfolio.id).filter_by(username=username).first()[0]
    balance: PortfolioBalance = (
        db.query(PortfolioBalance)
        .filter_by(portfolio_id=portfolio_id, currency=currency)
        .one_or_none()
    )
    timestamp = datetime.now()

    if balance:
        balance.amount = PortfolioBalance.amount + amount
        db.add(balance)
    else:
        balance = PortfolioBalance(
            currency=currency,
            amount=amount,
            timestamp=timestamp,
            portfolio_id=portfolio_id,
        )
        db.add(balance)
    db.commit()


def subtract_amount_from_currency(
    username: str, currency: str, amount: float, db: Callable[..., Session] = get_db()
) -> None:

    """
    Subtract amount from currency for user

    Args:
        username: The username.
        currency: The currency code of money being added.
        amount: The amount of money being added.
        db: A function that returns a `Session` object.

    Raises:
        ValueError
    """
    portfolio_id = db.query(Portfolio.id).filter_by(username=username)
    balance: PortfolioBalance = (
        db.query(PortfolioBalance)
        .filter_by(portfolio_id=portfolio_id, currency=currency)
        .one_or_none()
    )
    if balance:
        balance.amount = PortfolioBalance.amount - amount
        db.add(balance)
        db.commit()
    else:
        raise ValueError  # TODO another custom exception here?


def add_balances_to_portfolio_balance_table(
    username: str, currency_balances: dict[str, float]
) -> None:
    """
    Add amount to currency (for currency in balance map) for user if currency exists else
    create currency in portfolio for user with value of amount
    """

    for currency, amount in currency_balances.items():
        add_amount_to_currency(username=username, currency=currency, amount=amount)


create_tables()
