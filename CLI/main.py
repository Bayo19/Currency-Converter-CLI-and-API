import sys
import typer
import rich
from rich.table import Table
from rich.console import Console
from fuzzywuzzy import process
from common.convert import FXConverter
from common.utility_functions import ingest_rates, get_country_code
from db.database_functions import add_rates_to_table, drop_and_create_rates_table

app = typer.Typer()


def run_application(application, command):
    valid_commands = ["convert-currency", "download-latest-rates", "country-code"]
    suggestions = process.extract(command, valid_commands, limit=1)

    if command not in valid_commands and suggestions[0][1] > 60:
        rich.print(
            f"No such command: [white]'{command}'[/white]. Did you mean: [yellow]{suggestions[0][0]}[/yellow]"
        )
    else:
        application()


@app.command()
def convert_currency(
    amount: float = typer.Argument(
        ..., help="The amount of money to convert", show_default=False
    ),
    source_currency: str = typer.Option(default="USD", help="Currency to convert from"),
    target_currency: str = typer.Option(default="GBP", help="Currency to convert to"),
):
    """Converts currency"""
    console = Console()
    result_table = Table(title="\nCurrency Conversion")

    converter = FXConverter()
    result = converter.convert_currency_(
        amount=amount, source_currency_code=source_currency, target_currency_code=target_currency
    )
    if result is None:
        rich.print("[bold red] Please use a valid currency name [/bold red]")
        rich.print(
            "[red] To find a countrys currency name, use the command [/red]: [yellow] country-code [/yellow]"
        )
        raise typer.Exit()

    result_table.add_column(result.source_currency_code, style="rgb(175,0,255)")
    result_table.add_column(result.target_currency_code, style="green")
    requested = "{:.2f}".format(result.requested_amount)
    converted = "{:.2f}".format(result.converted_amount)
    result_table.add_row(
        f"{requested} {result.source_currency_code}",
        f"{converted} {result.target_currency_code}",
    )
    console.print(result_table)


@app.command()
def download_latest_rates():
    """
    Downloads the latest exchange rates from openexchangerates.org
    to make them available for conversion queries
    """
    data = ingest_rates()
    drop_and_create_rates_table()
    add_rates_to_table(data=data)
    rich.print(
        "[bold green] Today's exchange rates have finished downloading [/bold green]"
    )


@app.command()
def country_code(
    country: str = typer.Argument(
        ..., help="Search for a country code using the country name", show_default=False
    )
):
    """
    Displays a table containing a country and it's currency code given the country
    """

    result = get_country_code(country)
    console = Console()
    table = Table("country", "currency code")

    if result is not None:
        table.add_row(result.country, result.country_code)
        console.print(table)
    else:
        console.print("Please enter a valid country")
        rich.print("Try[red] 'main.py country-code --help' [/red]for help.")


if __name__ == "__main__":
    run_application(application=app, command=sys.argv[1])
