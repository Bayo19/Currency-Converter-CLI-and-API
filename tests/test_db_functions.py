from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.db.models import Rate, Portfolio, PortfolioBalance
from src.db.database_functions import (
    add_rates_to_table,
    get_rates_from_table,
    get_portfolio_from_table,
    user_exists,
    create_new_portfolio_user,
    add_amount_to_currency,
    subtract_amount_from_currency,
)
from src.common.data_types import CurrencyRate
from tests.fixtures import database, temp_db


def test_add_rates_to_table(database: Session, temp_db):
    add_rates_to_table(
        data=[
            CurrencyRate(code="EUR", rate=0.93953),
            CurrencyRate(code="GBP", rate=0.831098),
            CurrencyRate(code="JPY", rate=134.78133333),
            CurrencyRate(code="NGN", rate=460),
            CurrencyRate(code="USD", rate=1),
        ],
        db=database,
    )

    assert (
        database.query(Rate)
        .filter(
            or_(
                Rate.currency_code == "EUR",
                Rate.currency_code == "USD",
                Rate.currency_code == "GBP",
            )
        )
        .count()
        == 3
    )


def test_get_rates_from_table(database: Session, temp_db):
    add_rates_to_table(
        data=[
            CurrencyRate(code="EUR", rate=0.93953),
            CurrencyRate(code="GBP", rate=0.831098),
            CurrencyRate(code="JPY", rate=134.78133333),
            CurrencyRate(code="NGN", rate=460),
            CurrencyRate(code="USD", rate=1),
        ],
        db=database,
    )
    response = get_rates_from_table(from_rate="USD", to_rate="GBP", db=database)
    assert "USD" and "GBP" in response


def test_get_portfolio_from_table(database: Session, temp_db):
    portfolio_post = Portfolio(username="Jerry")
    database.add(portfolio_post)
    database.commit()
    portfolio_id = database.query(Portfolio.id).filter_by(username="Jerry").first()[0]
    balance = PortfolioBalance(
        currency="EUR",
        amount=300,
        timestamp=datetime.now(),
        portfolio_id=portfolio_id,
    )
    database.add(balance)
    database.commit()
    p = get_portfolio_from_table(username="Jerry", db=database)
    user_portfolio = p[0]

    assert user_portfolio.username == "Jerry"
    assert user_portfolio.amount == 300.0
    assert user_portfolio.currency_code == "EUR"


def test_user_exists(database: Session, temp_db):
    portfolio_post = Portfolio(username="Xavier")
    database.add(portfolio_post)
    database.commit()
    portfolio_id = database.query(Portfolio.id).filter_by(username="Xavier").first()[0]
    balance = PortfolioBalance(
        currency="EUR",
        amount=300,
        timestamp=datetime.now(),
        portfolio_id=portfolio_id,
    )
    database.add(balance)
    database.commit()

    assert user_exists(username="Bob", db=database) == False
    assert user_exists(username="Xavier", db=database) == True


def test_new_portfolio_user(database: Session, temp_db):
    creation = create_new_portfolio_user(username="Goliath", db=database)
    assert creation == True
    assert user_exists(username="Goliath", db=database) == True
    second_creation = create_new_portfolio_user(username="Goliath", db=database)
    assert second_creation == False


def test_add_amount_to_currency(database: Session, temp_db):
    portfolio_post = Portfolio(username="Jiang")
    database.add(portfolio_post)
    database.commit()
    portfolio_id = database.query(Portfolio.id).filter_by(username="Jiang").first()[0]
    balance = PortfolioBalance(
        currency="EUR",
        amount=300,
        timestamp=datetime.now(),
        portfolio_id=portfolio_id,
    )
    database.add(balance)
    database.commit()
    add_amount_to_currency(username="Jiang", currency="EUR", amount=250.0, db=database)
    p = get_portfolio_from_table(username="Jiang", db=database)
    user_portfolio = p[0]
    assert user_portfolio.amount == 550.0


def test_subtract_amount_from_currency(database: Session, temp_db):
    portfolio_post = Portfolio(username="Jiang")
    database.add(portfolio_post)
    database.commit()
    portfolio_id = database.query(Portfolio.id).filter_by(username="Jiang").first()[0]
    balance = PortfolioBalance(
        currency="EUR",
        amount=300,
        timestamp=datetime.now(),
        portfolio_id=portfolio_id,
    )
    database.add(balance)
    database.commit()
    subtract_amount_from_currency(
        username="Jiang", currency="EUR", amount=70.0, db=database
    )
    p = get_portfolio_from_table(username="Jiang", db=database)
    user_portfolio = p[0]
    assert user_portfolio.amount == 230.0
