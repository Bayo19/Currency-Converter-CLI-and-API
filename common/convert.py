from typing import Union
from db.database_functions import get_rates_from_table
from common.data_types import CurrencyConversion


class FXConverter:
    def __init__(self) -> None:
        ...

    def convert_currency_(
        self,
        amount: float,
        source_currency: str,
        target_currency: str,
    ) -> Union[CurrencyConversion, None]:

        """
        Converts currency

        Args:
            amount: Amount of money in
        """
        try:
            rates = get_rates_from_table(
                from_rate=source_currency, to_rate=target_currency
            )
        except ValueError:
            return None

        return CurrencyConversion(
            from_currency=source_currency,
            to_currency=target_currency,
            requested_amount=amount,
            converted_amount=(amount * rates.get(target_currency))
            / rates.get(source_currency),
        )
