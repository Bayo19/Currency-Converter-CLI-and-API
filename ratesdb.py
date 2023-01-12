import sqlite3
from typing import List, Callable, Any
from sqlite3 import Connection
from utilities import CurrencyRate


def init_db(fn: Callable[..., Any]) -> Callable[..., Any]:
    initialised = False
    con = sqlite3.connect("rates.db")
    cur = con.cursor()
    if initialised is False:
        cur.execute("CREATE TABLE IF NOT EXISTS exchangerates(currencycode, rate)")
        initialised = True

    def inner(*args, **kwargs):
        return fn(connection=con, *args, **kwargs)

    return inner


@init_db
def rates_to_db(connection: Connection, data: List[CurrencyRate]) -> None:
    cur = connection.cursor()
    cur.executemany("INSERT INTO exchangerates VALUES(?, ?)", data)
    connection.commit()
    connection.close()


@init_db
def get_rates(connection: Connection, query: str, query_params: tuple) -> list:
    cur = connection.cursor()
    res = cur.execute(query, query_params)
    result = res.fetchall()
    connection.close()
    return result
