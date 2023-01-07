import typer
import json
import rich
from rich.console import Console
from rich.table import Table


class FXConverter:
    def __init__(
        self,
        rates_file_path: str = "./rates.json",
    ) -> None:
    
        with open(rates_file_path, "r") as rates_json:
            self.rates = json.load(rates_json).get("rates")
        self.console = Console()
        self.currency_table = Table("Currency Names")

        for key in self.rates:
            self.currency_table.add_row(key)

    def convert_currency_(
        self,
        amount: int,
        convert: str,
        to: str,
    ):
        """
        Convert currency
        """
        if amount is None:
            amount = self.amount
        if convert is None:
            convert = self.convert
        if to is None:
            to = self.to
        if not self.rates.get(convert) or self.rates.get(to) is None:
            rich.print("[bold red] Please use a valid currency name [/bold red]")
            rich.print(
                "[red] To see valid currency names, use the command [/red]: [yellow] valid-currency-names [/yellow]"
            )
            raise typer.Exit()

        amount_in_new_currency = "{:.2f}".format(
            (amount * self.rates.get(to)) / self.rates.get(convert)
        )
        result_table = Table(title="\nCurrency Conversion")
        result_table.add_column(convert, style="rgb(175,0,255)")
        result_table.add_column(to, style="green")
        result_table.add_row(f"{amount} {convert}", f"{amount_in_new_currency} {to}")
        self.console.print(result_table)
