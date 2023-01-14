import pytest
from src.utilities import CurrencyConversion
from src.convert import FXConverter


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
                new_amount="{:.2f}".format(408.80),
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
                new_amount="{:.2f}".format(444.29),
            ),
        ),
        (
            1000,
            "GBP",
            "USD",
            CurrencyConversion(
                convert_from="GBP",
                convert_to="USD",
                original_amount=1000,
                new_amount="{:.2f}".format(1223.10),
            ),
        ),
        (
            50,
            "GBP",
            "JPY",
            CurrencyConversion(
                convert_from="GBP",
                convert_to="JPY",
                original_amount=50,
                new_amount="{:.2f}".format(7821.41),
            ),
        ),
        (135, "USD", "ZZZ", None),
        (200_069_420, "ZZZ", "USD", None),
    ],
)
def test_convert_currency(amount, convert, to, expected):
    converter = FXConverter()
    result = converter.convert_currency_(amount=amount, convert=convert, to=to)
    assert result == expected
