from collections import namedtuple

CurrencyConversion = namedtuple(
    "CurrencyConversion", "from_currency to_currency requested_amount converted_amount"
)
CountryCode = namedtuple("CountryCode", "country country_code")

CurrencyRate = namedtuple("CurrencyRate", "code rate")
