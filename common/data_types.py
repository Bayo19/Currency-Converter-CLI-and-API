from dataclasses import dataclass
from datetime import datetime

@dataclass
class CurrencyConversion:
    from_currency: str
    to_currency: str
    requested_amount: float
    converted_amount: float


@dataclass
class CountryCode:
    country: str
    country_code: str


@dataclass
class CurrencyRate:
    code: str
    rate: float

@dataclass
class PortfolioItem:
    username: str
    user_id: int
    currency_code: str
    amount: str
    timestamp: datetime