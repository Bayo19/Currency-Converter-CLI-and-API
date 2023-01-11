import sqlite3
from typing import List
from sqlite3 import Connection, Cursor
from command_functions import ingest_rates
from utilities import CurrencyRate

con = sqlite3.connect("rates.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS exchangerates(currencycode, rate)")

def rates_to_db(connection: Connection, data: List[CurrencyRate]) -> None:
    cur = connection.cursor()
    cur.executemany("INSERT INTO exchangerates VALUES(?, ?)", data)
    connection.commit()
    print("Rates now in database")

def get_rates(connection: Connection, query: str) -> list:
    cur = connection.cursor()
    res = cur.execute(query)
    return res.fetchall()
