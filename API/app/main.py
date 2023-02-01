from fastapi import FastAPI, Query

app = FastAPI()

# http://127.0.0.1:8000/convert/?from_currency=USD&to_currency=GBP&amount=400
@app.get("/convert/")
def conversion(
    amount: int,
    to_currency: str = Query(default=..., max_length=3),
    from_currency: str = Query(default="USD", max_length=3),
):
    return from_currency, to_currency, amount
