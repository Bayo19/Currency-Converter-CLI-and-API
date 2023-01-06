import typer
from convert import FXConverter

app = typer.Typer()


@app.command()
def start_conversion(
    amount: int = typer.Argument(1),
    convert: str = typer.Option(default="USD", help="Currency to convert from"),
    to: str = typer.Option(default="GBP", help="Currency to convert to"),
):
    converter = FXConverter(amount=amount, convert=convert, to=to)
    converter.convert_currency()


if __name__ == "__main__":
    app()
