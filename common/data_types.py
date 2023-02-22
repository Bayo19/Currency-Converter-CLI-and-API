from dataclasses import dataclass


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


class CurrencyRate:
    code: str
    rate: float
