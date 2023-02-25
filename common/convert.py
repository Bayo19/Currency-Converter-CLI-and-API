from typing import Union
from db.database_functions import get_rates_from_table
from common.data_types import CurrencyConversion


class FXConverter:
    def __init__(self) -> None:
        ...

    def convert_currency_(
        self,
        amount: float,
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
            from_currency=convert,
            to_currency=to,
            requested_amount=amount,
            converted_amount=(amount * rates.get(to)) / rates.get(convert),
        )
