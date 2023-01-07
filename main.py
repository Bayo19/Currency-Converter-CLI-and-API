import typer
from convert import FXConverter
from command_functions import ingest_rates, get_country_code

app = typer.Typer()


@app.command()
def convert_currency(
    amount: int = typer.Argument(..., help="The amount of money to convert", show_default=False),
    convert: str = typer.Option(default="USD", help="Currency to convert from"),
    to: str = typer.Option(default="GBP", help="Currency to convert to"),
):
    """Converts currency"""
    converter = FXConverter()
    converter.convert_currency_(amount=amount, convert=convert, to=to)


@app.command()
def download_latest_rates():
    """
    Downloads the latest exchange rates from openexchangerates.org
    to make them available for conversion queries
    """
    ingest_rates()


@app.command()
def country_code(country: str = typer.Argument(...,help="Search for a country code using the country name", show_default=False)):
    """
    Displays a table containing a country and it's currency code given the country
    """
    get_country_code(country)


if __name__ == "__main__":
    app()
