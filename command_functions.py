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

    filtered_codes = {
        k: v for k, v in country_currency_codes.items() if country.upper() in k
    }
    code = list(v for v in filtered_codes.values())[
        0
    ]  # the key for the code doesn't always match the param: country
    return CountryCode(country=country.upper(), country_code=code)


get_country_code("france")
