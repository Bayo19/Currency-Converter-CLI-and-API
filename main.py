import typer
from convert import FXConverter
from command_functions import ingest_rates, get_valid_names

app = typer.Typer()


@app.command()
def convert_currency(
    amount: int = typer.Argument(1),
    convert: str = typer.Option(default="USD", help="Currency to convert from"),
    to: str = typer.Option(default="GBP", help="Currency to convert to"),
):
    converter = FXConverter(amount=amount, convert=convert, to=to)
    converter.convert_currency_()


@app.command()
def download_todays_rates():
    ingest_rates()


@app.command()
def valid_currency_names(
    first_letter: str = typer.Argument("A", help="first letter of currency acronym")
):
    get_valid_names(first_letter)


if __name__ == "__main__":
    app()
