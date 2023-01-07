from bs4 import BeautifulSoup
import requests

html = requests.get("https://www.iban.com/currency-codes")
soup = BeautifulSoup(html.text, "html.parser")
table = soup.find("tbody")
rows = table.find_all("tr")
_rows = [
    [
        item.replace("<td>", "").replace("</td>", "")
        for item in str(row).splitlines()[1:-1]
    ]
    for row in rows
]

country_currency_codes = {}

for row in _rows:
    country_currency_codes[row[0]] = row[2]
