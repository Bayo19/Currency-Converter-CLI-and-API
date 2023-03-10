import pytest
from common.data_types import CurrencyConversion
from common.convert import FXConverter
from unittest.mock import patch


@pytest.mark.parametrize(
    "amount, source_currency_code, target_currency_code, expected",
    [
        (
            500,
            "USD",
            "GBP",
            CurrencyConversion(
                source_currency_code="USD",
                target_currency_code="GBP",
                requested_amount=500,
                converted_amount=421.02250000000004,
            ),
        ),
        (
            69_500,
            "JPY",
            "GBP",
            CurrencyConversion(
                source_currency_code="JPY",
                target_currency_code="GBP",
                requested_amount=69_500,
                converted_amount=427.8624507321724,
            ),
        ),
        (
            1000,
            "GBP",
            "USD",
            CurrencyConversion(
                source_currency_code="GBP",
                target_currency_code="USD",
                requested_amount=1000,
                converted_amount=1187.5849865506,
            ),
        ),
        (
            50,
            "GBP",
            "JPY",
            CurrencyConversion(
                source_currency_code="GBP",
                target_currency_code="JPY",
                requested_amount=50,
                converted_amount=8121.7690265959645,
            ),
        ),
        (135, "USD", "ZZZ", None),
        (200_069_420, "ZZZ", "USD", None),
    ],
)
def test_convert_currency(
    amount: float, source_currency_code: str, target_currency_code: str, expected
):
    def mock_get_rates_func(from_rate, to_rate):
        rates_dict = {"GBP": 0.806753, "JPY": 128.127, "EUR": 0.920924}
        if from_rate not in rates_dict or to_rate not in rates_dict:
            raise ValueError
        return {k: v for k, v in rates_dict if k == from_rate or k == to_rate}

    p = patch("common.convert.get_rates_from_table", new=mock_get_rates_func)
    converter = FXConverter()
    result = converter.convert_currency_(
        amount=amount,
        source_currency_code=source_currency_code,
        target_currency_code=target_currency_code,
    )
    assert result == expected
