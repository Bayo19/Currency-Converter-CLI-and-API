from collections import namedtuple

CurrencyConversion = namedtuple(
    "CurrencyConversion", "convert_from, convert_to original_amount new_amount"
)
CountryCode = namedtuple("CountryCode", "country country_code")

CurrencyRate = namedtuple("CurrencyRate", "code rate")


def run_once(func):
    def inner(*args, **kwargs):
        if not inner.has_run:
            result = func(*args, **kwargs)
            inner.has_run = True
            return result

    inner.has_run = False
    return inner
