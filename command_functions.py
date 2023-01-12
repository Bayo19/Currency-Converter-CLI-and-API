import os
import requests
import api_keys
from country_codes_mapping import country_currency_codes
from utilities import CountryCode, CurrencyRate
from typing import List

def ingest_rates() -> List[CurrencyRate]:
    """
    Downloads the latest exchange rates from openexchangerates.org and writes them to rates.json
    to make them available for conversion queries
    """
    api_key = os.environ["API_KEY"]
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url, headers={"accept": "application/json"})

    rates = [CurrencyRate(code=k, rate=v) for k, v in response.json()["rates"].items()]
    return rates


ingest_rates()


def get_country_code(country: str) -> CountryCode:
    """
    Returns a country code
    """

    filtered_codes = {
        k: v for k, v in country_currency_codes.items() if country.upper() in k
    }
    code = list(v for v in filtered_codes.values())[
        0
    ]  # the key for the code doesn't always match the param: country
    return CountryCode(country=country.upper(), country_code=code)
