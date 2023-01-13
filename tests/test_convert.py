import pytest
from ..src.utilities import CurrencyConversion
from ..src.convert import FXConverter


@pytest.mark.parametrize(
    "amount, convert, to, expected",
    [
        (
            500,
            "USD",
            "GBP",
            CurrencyConversion(
                convert_from="USD",
                convert_to="GBP",
                original_amount=500,
                new_amount="{:.2f}".format(413.46),
            ),
        ),
        (
            69_500,
            "JPY",
            "GBP",
            CurrencyConversion(
                convert_from="JPY",
                convert_to="GBP",
                original_amount=69_500,
                new_amount="{:.2f}".format(435.11),
            ),
        ),
    ],
)
def test_convert_currency(amount, convert, to, expected):
    converter = FXConverter()
    result = converter.convert_currency_(amount=amount, convert=convert, to=to)
    assert result == expected
