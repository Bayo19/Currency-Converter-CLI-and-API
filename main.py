import typer
import json

app = typer.Typer()

with open("./rates.json", "r") as rates_json:
    rates = json.load(rates_json)

rates_dict = rates[0]
for dictionary in rates[1:]:
    rates_dict.update(dictionary["rates"])


@app.command()
def convert_currency(
    amount: int = typer.Argument(1),
    from_: str = typer.Option(default="USD", help="Currency to convert from"),
    to: str = typer.Option(default="GBP", help="Currency to convert to"),
):
    print(amount, from_, to)

# TODO - understand why with one command I don't need to specify the command in the terminal when using the CLI
# TODO - add logic to get rates from rates_dict and display the currency conversion showing the from and to.
# TODO - if the rate doesn't exist, show a suitable message and exit 

if __name__ == "__main__":
    app()
