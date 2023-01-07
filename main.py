import typer
from convert import FXConverter
from command_functions import ingest_rates, get_valid_names

app = typer.Typer()


@app.command()
def convert_currency(
    amount: int,
    convert: str = typer.Option(default="USD"),
    to: str = typer.Option(default="GBP"),
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
def valid_currency_names(
    first_letter: str = typer.Argument(
        default="A", help="first letter of currency acronym"
    )
):
    """
    Returns a table containing list of valid currency names
    """
    if len(first_letter) > 1:
        raise typer.Exit()
    get_valid_names(first_letter)


if __name__ == "__main__":
    app()
