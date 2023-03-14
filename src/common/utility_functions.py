from typing import List, Union
import requests
from common.api_keys import api_key
from common.country_codes_mapping import country_currency_codes
from common.data_types import CountryCode, CurrencyRate, PortfolioItem
from db.database_functions import (
    subtract_amount_from_currency,
    add_amount_to_currency,
)


def ingest_rates() -> List[CurrencyRate]:
    """
    Downloads the latest exchange rates from openexchangerates.org
    and writes them to rates.json to make them available for conversion queries
    """
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url, headers={"accept": "application/json"})

    rates = [CurrencyRate(code=k, rate=v) for k, v in response.json()["rates"].items()]
    return rates


def get_country_code(country: str) -> Union[CountryCode, None]:
    """
    Returns a country code
    """

    filtered_codes = {
        k: v for k, v in country_currency_codes.items() if country.upper() in k
    }
    try:
        code = list(v for v in filtered_codes.values())[0]
    except IndexError:
        return None
    # the key for the code doesn't always match the param: country
    return CountryCode(country=country.upper(), country_code=code)


def valid_trade(
    buyer_portfolio: list[PortfolioItem],
    seller_portfolio: list[PortfolioItem],
    buyer_currency_code,
    seller_currency_code: str,
    buyer_amount: float,
    seller_amount: float,
) -> bool:

    seller_has_enough_money = bool(
        [
            t
            for t in seller_portfolio
            if t.currency_code == seller_currency_code and t.amount >= seller_amount
        ]
    )

    buyer_has_enough_money = bool(
        [
            s
            for s in buyer_portfolio
            if s.currency_code == buyer_currency_code and s.amount >= buyer_amount
        ]
    )

    return bool(seller_has_enough_money and buyer_has_enough_money)


def trade(
    buyer_currency_code: str,
    seller_currency_code: str,
    buyer_amount: float,
    seller_amount: float,
    buyer_username: str,
    seller_username,
) -> None:
    subtract_amount_from_currency(
        username=buyer_username,
        currency=buyer_currency_code,
        amount=buyer_amount,
    )
    add_amount_to_currency(
        username=seller_username,
        currency=buyer_currency_code,
        amount=buyer_amount,
    )

    subtract_amount_from_currency(
        username=seller_username,
        currency=seller_currency_code,
        amount=seller_amount,
    )
    add_amount_to_currency(
        username=buyer_username,
        currency=seller_currency_code,
        amount=seller_amount,
    )


def run_once(func):
    def inner(*args, **kwargs):
        if not inner.has_run:
            result = func(*args, **kwargs)
            inner.has_run = True
            return result

    inner.has_run = False
    return inner
