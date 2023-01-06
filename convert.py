import typer
import json
from rich.console import Console
from rich.table import Table


class FXConverter:
    def __init__(
        self,
        amount: int,
        convert: str = typer.Option(default="USD", help="Currency to convert from"),
        to: str = typer.Option(default="GBP", help="Currency to convert to"),
        rates_file_path: str = "./rates.json",
    ) -> None:

        with open(rates_file_path, "r") as rates_json:
            self.rates = {
                k: v
                for d in [d["rates"] for d in json.load(rates_json)]
                for k, v in d.items()
            }
        self.console = Console()
        self.currency_table = Table("Currency Names")
        self.amount = amount
        self.convert = convert
        self.to = to

        for key in self.rates:
            self.currency_table.add_row(key)

    def convert_currency(
        self,
        amount: int = None,
        convert: str = None,
        to: str = None,
    ):
        if amount is None:
            amount = self.amount
        if convert is None:
            convert = self.convert
        if to is None:
            to = self.to
        if not self.rates.get(convert) or self.rates.get(to) is None:
            print("Please use a valid currency name")
            self.console.print(self.currency_table)
            raise typer.Exit()

        amount_in_new_currency = "{:.2f}".format(
            (amount * self.rates.get(to)) / self.rates.get(convert)
        )
        print(f"{amount} {convert} is {amount_in_new_currency} {to}")
