import json
import os
import requests
import api_keys
from .country_codes_mapping import country_currency_codes
from .utilities import CountryCode


def ingest_rates() -> str:
    """
    Downloads the latest exchange rates from openexchangerates.org and writes them to rates.json
    to make them available for conversion queries
    """
    api_key = os.environ["API_KEY"]
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url, headers={"accept": "application/json"})

    with open("./rates.json", "w") as rates_json:
        rates_json.write(response.text)

    return "Today's exchange rates have finished downloading"


def get_country_code(country: str) -> CountryCode:
    """
    Returns a country code
    """

    with open("./rates.json", "r") as r_json:
        rates = json.load(r_json).get("rates")

    filtered_codes = dict(
        filter(lambda elem: country.upper() in elem[0], country_currency_codes.items())
    )

    code = tuple(filtered_codes.popitem())[1]
    return CountryCode(country=country.upper(), country_code=code)
