import json
import os
import requests
import api_keys
from rich import print as _print
from rich.table import Table
from rich.console import Console
import json

def ingest_rates():
    api_key = os.environ["API_KEY"]
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url, headers={"accept": "application/json"})

    with open("./rates.json", "w") as rates_json:
        rates_json.write(json.dumps(response.json()))
    
    _print("[bold green] Today's exchange rates have finished downloading [/bold green]")

def get_valid_names() -> None:
    """
    Returns a table containing names of valid currency names
    """
    console = Console()
    with open("./rates.json", "r") as r_json:
        rates = json.load(r_json).get("rates")
        currency_table = Table("Currency Names")
        for key in rates:
                currency_table.add_row(key)
        console.print(currency_table)