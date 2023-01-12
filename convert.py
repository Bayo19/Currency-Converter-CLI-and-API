from typing import Union
from utilities import CurrencyConversion
from ratesdb import con as _con, get_rates


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
        conversion_params = (convert, to)
        db_query = (
            f"SELECT * FROM exchangerates WHERE currencycode = ? OR currencycode = ?"
        )
        rates = dict(
            get_rates(connection=_con, query=db_query, query_params=conversion_params)
        )

        return CurrencyConversion(
            convert_from=convert,
            convert_to=to,
            original_amount=amount,
            new_amount="{:.2f}".format((amount * rates.get(to)) / rates.get(convert)),
        )
