from typing import Union
from src.db.database_functions import get_rates_from_table
from src.common.data_types import CurrencyConversion


class FXConverter:
    def __init__(self) -> None:
        ...

    def convert_currency_(
        self,
        amount: float,
        source_currency_code: str,
        target_currency_code: str,
    ) -> Union[CurrencyConversion, None]:

        """
        Converts currency

        Args:
            amount: Amount of money in
        """
        try:
            rates = get_rates_from_table(
                from_rate=source_currency_code, to_rate=target_currency_code
            )
        except ValueError:
            return None

        return CurrencyConversion(
            source_currency_code=source_currency_code,
            target_currency_code=target_currency_code,
            requested_amount=amount,
            converted_amount=(amount * rates.get(target_currency_code))
            / rates.get(source_currency_code),
        )
