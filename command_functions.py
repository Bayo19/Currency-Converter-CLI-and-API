import json
import os
import requests
import api_keys
import rich
from rich.table import Table
from rich.console import Console
import json


def ingest_rates():
    """
    Downloads the latest exchange rates from openexchangerates.org and writes them to rates.json
    to make them available for conversion queries
    """
    api_key = os.environ["API_KEY"]
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url, headers={"accept": "application/json"})

    with open("./rates.json", "w") as rates_json:
        rates_json.write(json.dumps(response.json()))

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
