from pydantic import BaseModel
from datetime import datetime


class Conversion(BaseModel):
    from_currency: str
    to_currency: str
    requested_amount: int
    converted_amount: int

    class Config:
        orm_mode = True


class ConversionData(BaseModel):
    timestamp: datetime
    conversion: Conversion

    class Config:
        orm_mode = True


class UserPortfolio(BaseModel):
    user_id: int
    currencies: dict[str, float]
    timestamp: datetime

    class Config:
        orm_mode = True


class CreatePortfolio(BaseModel):
    username: str
    currency_balances: dict[str, float]

    class Config:
        orm_mode = True


class Trade(BaseModel):
    buyer_name: str
    seller_name: str
    target_currency: str
    amount: float
    timestamp: datetime
