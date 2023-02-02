from datetime import datetime
from fastapi import FastAPI, Query
from common import convert

app = FastAPI()

@app.get("/convert/")
def conversion(
    amount: int,
    to_currency: str = Query(default=..., max_length=3),
    from_currency: str = Query(default="USD", max_length=3),
):
    converter = convert.FXConverter()
    timestamp = datetime.now()
    conversion_response = dict()
    conversion_response["timestamp"] = timestamp
    conversion_response["conversion"] = converter.convert_currency_(
        amount=amount, convert=from_currency, to=to_currency
    )._asdict()

    return conversion_response
