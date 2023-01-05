import typer
import json
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

with open("./rates.json", "r") as rates_json:
    rates = json.load(rates_json)

_rates = {k:v for d in [d["rates"] for d in rates] for k,v in d.items()}

currency_table = Table("Currency Names")
for key in _rates:
    currency_table.add_row(key)

@app.command()
def convert_currency(
    amount: int = typer.Argument(1),
    from_: str = typer.Option(default="USD", help="Currency to convert from"),
    to: str = typer.Option(default="GBP", help="Currency to convert to"),
):  
    if not _rates.get(from_) or _rates.get(to) is None:
        print("Please use a valid currency name")
        console.print(currency_table)
        raise typer.Exit()

    amount_in_new_currency = "{:.2f}".format((amount * _rates.get(to)) / _rates.get(from_))
    print(f"{amount} {from_} is {amount_in_new_currency} {to}")


if __name__ == "__main__":
    app()
