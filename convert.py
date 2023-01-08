import json
from typing import Union
from utilities import CurrencyConversion


class FXConverter:
    def __init__(
        self,
        rates_file_path: str = "./rates.json",
    ) -> None:

        with open(rates_file_path, "r") as rates_json:
            self.rates = json.load(rates_json).get("rates")

    def convert_currency_(
        self,
        amount: int,
        convert: str,
        to: str,
    ) -> Union[CurrencyConversion, None]:
        """
        Converts currency
        """
        if amount is None:
            amount = self.amount
        if convert is None:
            convert = self.convert
        if to is None:
            to = self.to
        if not self.rates.get(convert) or self.rates.get(to) is None:
            return None

        return CurrencyConversion(
            convert_from=convert,
            convert_to=to,
            original_amount=amount,
            new_amount="{:.2f}".format(
                (amount * self.rates.get(to)) / self.rates.get(convert)
            ),
        )
