from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import Session
from db.models import Rate, Portfolio, PortfolioBalance
from db.database_functions import add_rates_to_table, get_rates_from_table, get_portfolio_from_table
from common.data_types import CurrencyRate
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
    