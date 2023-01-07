import json
import os
import requests
import rich
from rich.table import Table
from rich.console import Console
import json
import api_keys
from country_codes_mapping import country_currency_codes


def ingest_rates() -> None:
    """
    Downloads the latest exchange rates from openexchangerates.org and writes them to rates.json
    to make them available for conversion queries
    """
    api_key = os.environ["API_KEY"]
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url, headers={"accept": "application/json"})

    with open("./rates.json", "w") as rates_json:
        rates_json.write(response.text)

    rich.print(
        "[bold green] Today's exchange rates have finished downloading [/bold green]"
    )


def get_valid_names(letter: str = "A") -> None:
    """
    Returns a table containing list of valid currency names
    """
    _letter = letter.upper()
    console = Console()

    with open("./rates.json", "r") as r_json:
        rates = json.load(r_json).get("rates")
        currency_table = Table("Currency Names")

    for key in rates:
        if key[0] == _letter:
            currency_table.add_row(key)

    console.print(currency_table)


def get_country_code(country: str) -> None:
    """
    Returns a table containing a country and it's currency code given the country
    """
    console = Console()
    table = Table("country", "currency code")

    with open("./rates.json", "r") as r_json:
        rates = json.load(r_json).get("rates")

    filtered_codes = dict(
        filter(lambda elem: country.upper() in elem[0], country_currency_codes.items())
    )

    row = tuple(filtered_codes.popitem())
    table.add_row(country.upper(), row[1])
    console.print(table)
