from datetime import datetime
from typing import Any
from fastapi import FastAPI, Query, status, HTTPException
from common import convert, portfolio
from db.schemas import UserPortfolio, ConversionData, CreatePortfolio

app = FastAPI()


@app.get("/convert/", status_code=status.HTTP_200_OK)
def conversion(
    amount: int,
    to_currency: str = Query(default=..., max_length=3),
    from_currency: str = Query(default="USD", max_length=3),
) -> ConversionData:
    converter = convert.FXConverter()
    conversion_result = converter.convert_currency_(
        amount=amount, convert=from_currency, to=to_currency
    )
    if conversion_result:
        timestamp = datetime.now()
        conversion_response = {
            "timestamp": timestamp,
            "conversion": conversion_result,
        }
        return conversion_response
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="One or both of the given currency codes is not valid",
    )


@app.post("/create_portfolio/", status_code=status.HTTP_201_CREATED)
def initialise_portfolio(request: CreatePortfolio) -> dict[str, Any]:
    portf = portfolio.Portfolio(username=request.username)
    if portf.create_portfolio(balance_map=request.balance_map):
        return {"success": "true", "message": "Portfolio created", "x": request}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User: {request.username}, already exists.",
    )


@app.get("/portfolio/{username}", status_code=status.HTTP_200_OK)
def get_portfolio(username: str) -> UserPortfolio:
    portf = portfolio.Portfolio(username=username)
    portfolio_dict_result = portf.get_portfolio_as_dict()
    if portfolio_dict_result:
        return portfolio_dict_result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Username: {username} - does not exist",
    )


@app.put("/trade/{buyer_username}", status_code=status.HTTP_200_OK)
def make_trade(
    buyer_username: str,
    source_amount: int,
    seller_username: str,
    source_currency: str = Query(default=..., max_length=3),
    target_currency: str = Query(default=..., max_length=3),
) -> dict[str, Any]:
    portf = portfolio.Portfolio(username=buyer_username)

    currency_trade = portf.trade_currencies(
        source_currency_code=source_currency,
        target_currency_code=target_currency,
        source_amount=source_amount,
        other_portfolio_name=seller_username,
    )
    try:
        if currency_trade:

            timestamp = datetime.now()

            return {
                "success": "true",
                "message": "Trade successful",
                "details": {
                    "buyer": buyer_username,
                    "seller": seller_username,
                    "currency": target_currency,
                    "amount": source_amount,
                    "timestamp": timestamp,
                },
            }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Buyer or seller does not have enough of given currencies to trade given amount",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer or Seller or both do not exist",
        )
