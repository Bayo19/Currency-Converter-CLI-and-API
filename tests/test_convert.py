import pytest
from common.data_types import CurrencyConversion
from common.convert import FXConverter
from unittest.mock import patch


@pytest.mark.parametrize(
    "amount, convert, to, expected",
    [
        (
            500,
            "USD",
            "GBP",
            CurrencyConversion(
                from_currency="USD",
                to_currency="GBP",
                requested_amount=500,
                converted_amount="{:.2f}".format(403.38),
            ),
        ),
        (
            69_500,
            "JPY",
            "GBP",
            CurrencyConversion(
                from_currency="JPY",
                to_currency="GBP",
                requested_amount=69_500,
                converted_amount="{:.2f}".format(437.61),
            ),
        ),
        (
            1000,
            "GBP",
            "USD",
            CurrencyConversion(
                from_currency="GBP",
                to_currency="USD",
                requested_amount=1000,
                converted_amount="{:.2f}".format(1239.54),
            ),
        ),
        (
            50,
            "GBP",
            "JPY",
            CurrencyConversion(
                from_currency="GBP",
                to_currency="JPY",
                requested_amount=50,
                converted_amount="{:.2f}".format(7940.91),
            ),
        ),
        (135, "USD", "ZZZ", None),
        (200_069_420, "ZZZ", "USD", None),
    ],
)
def test_convert_currency(amount, convert, to, expected):
    def mock_get_rates_func(from_rate, to_rate):
        rates_dict = {"GBP": 0.806753, "JPY": 128.127, "EUR": 0.920924}
        if from_rate not in rates_dict or to_rate not in rates_dict:
            raise ValueError
        return {k: v for k, v in rates_dict if k == from_rate or k == to_rate}

    patch_mock_get_rates = patch(
        "common.convert.get_rates_from_table", new=mock_get_rates_func
    )
    converter = FXConverter()
    result = converter.convert_currency_(amount=amount, convert=convert, to=to)
    assert result == expected
