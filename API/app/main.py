from datetime import datetime
from typing import Any
from fastapi import FastAPI, Query, status, HTTPException, Depends
from common.convert import FXConverter
from common.portfolio import Portfolio
from db.schemas import UserPortfolio, ConversionData, CreatePortfolio, Trade

app = FastAPI()


def user_portfolio_instance(username: str) -> Portfolio:
    return Portfolio(username=username)


@app.get("/convert/", status_code=status.HTTP_200_OK)
def conversion(
    amount: int,
    to_currency: str = Query(default=..., max_length=3),
    from_currency: str = Query(default="USD", max_length=3),
) -> ConversionData:
    converter = FXConverter()
    conversion_result = converter.convert_currency_(
        amount=amount, source_currency_code=from_currency, target_currency_code=to_currency
    )
    if conversion_result:
        timestamp = datetime.now()
        return ConversionData(timestamp=timestamp, conversion=conversion_result)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="One or both of the given currency codes is not valid",
    )


@app.post("/create_portfolio/", status_code=status.HTTP_201_CREATED)
def initialise_portfolio(request: CreatePortfolio) -> CreatePortfolio:
    user_portfolio = Portfolio(
        username=request.username
    )  # not sure if I can use the dependency here
    if user_portfolio.create_portfolio(currency_balances=request.currency_balances):
        return request
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User: {request.username}, already exists.",
    )


@app.get("/portfolio/", status_code=status.HTTP_200_OK)
def get_portfolio(
    username: str, user_portfolio: Portfolio = Depends(user_portfolio_instance)
) -> UserPortfolio:
    portfolio_dict_result = user_portfolio.get_portfolio_as_dict()
    if portfolio_dict_result:
        return UserPortfolio(**portfolio_dict_result)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Username: {username} - does not exist",
    )


# make more idempotent by recording each trade and
# not allowing same trade to take place more than once?
@app.post("/trade/", status_code=status.HTTP_200_OK)
def make_trade(
    username: str,
    source_amount: float,
    seller_username: str,
    source_currency: str = Query(default=..., max_length=3),
    target_currency: str = Query(default=..., max_length=3),
    user_portfolio: Portfolio = Depends(user_portfolio_instance),
) -> Trade:

    currency_trade = user_portfolio.trade_currencies(
        buyer_currency_code=source_currency,
        seller_currency_code=target_currency,
        buyer_amount=source_amount,
        seller_portfolio_name=seller_username,
    )
    try:
        if currency_trade:

            timestamp = datetime.now()

            return Trade(**{
                    "buyer": username,
                    "seller": seller_username,
                    "target_currency": target_currency,
                    "amount": source_amount,
                    "timestamp": timestamp,
                })
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Buyer or seller does not have enough of given currencies to trade given amount",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer or Seller or both do not exist",
        )
