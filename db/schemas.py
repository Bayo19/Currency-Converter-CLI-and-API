from pydantic import BaseModel
from datetime import datetime


class Conversion(BaseModel):
    source_currency_code: str
    target_currency_code: str
    requested_amount: float
    converted_amount: float

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
    buyer: str
    seller: str
    target_currency: str
    amount: float
    timestamp: datetime
