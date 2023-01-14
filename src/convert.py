from typing import Union
from db.database_functions import get_rates_from_table
from utilities import CurrencyConversion


class FXConverter:
    def __init__(self) -> None:
        ...

    def convert_currency_(
        self,
        amount: int,
        convert: str,
        to: str,
    ) -> Union[CurrencyConversion, None]:

        """
        Converts currency
        """
        try:
            rates = get_rates_from_table(from_rate=convert, to_rate=to)
        except ValueError:
            return None

        return CurrencyConversion(
            convert_from=convert,
            convert_to=to,
            original_amount=amount,
            new_amount="{:.2f}".format((amount * rates.get(to)) / rates.get(convert)),
        )
