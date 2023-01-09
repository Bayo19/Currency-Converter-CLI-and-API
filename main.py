import typer
import rich
from rich.table import Table
from rich.console import Console
from convert import FXConverter
from command_functions import ingest_rates, get_country_code

app = typer.Typer()


@app.command()
def convert_currency(
    amount: int = typer.Argument(
        ..., help="The amount of money to convert", show_default=False
    ),
    convert: str = typer.Option(default="USD", help="Currency to convert from"),
    to: str = typer.Option(default="GBP", help="Currency to convert to"),
):
    """Converts currency"""
    console = Console()
    result_table = Table(title="\nCurrency Conversion")

    converter = FXConverter()
    result = converter.convert_currency_(amount=amount, convert=convert, to=to)
    if result is None:
        rich.print("[bold red] Please use a valid currency name [/bold red]")
        rich.print(
            "[red] To find a countrys currency name, use the command [/red]: [yellow] country-code [/yellow]"
        )
        raise typer.Exit()

    result_table.add_column(result.convert_from, style="rgb(175,0,255)")
    result_table.add_column(result.convert_to, style="green")
    result_table.add_row(
        f"{result.original_amount} {result.convert_from}",
        f"{result.new_amount} {result.convert_to}",
    )
    console.print(result_table)


@app.command()
def download_latest_rates():
    """
    Downloads the latest exchange rates from openexchangerates.org
    to make them available for conversion queries
    """
    result = ingest_rates()
    rich.print(f"[bold green] {result} [/bold green]")


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
    table.add_row(result.country, result.country_code)
    console.print(table)


if __name__ == "__main__":
    app()
