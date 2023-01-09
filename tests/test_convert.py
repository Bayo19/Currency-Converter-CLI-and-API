import pytest
from utilities import CurrencyConversion
from convert import FXConverter


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
        
    ],
)
def test_convert_currency(amount, convert, to, expected):
    converter = FXConverter()
    result = converter.convert_currency_(amount=amount, convert=convert, to=to)
    assert result == expected
