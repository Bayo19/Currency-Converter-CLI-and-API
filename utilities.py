from collections import namedtuple

CurrencyConversion = namedtuple(
    "CurrencyConversion", "convert_from, convert_to original_amount new_amount"
)
CountryCode = namedtuple("CountryCode", "country country_code")
