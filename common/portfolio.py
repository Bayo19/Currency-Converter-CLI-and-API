from typing import Any
from db.database_functions import (
    add_balances_to_portfolio_balance_table,
    create_new_portfolio_user,
)

"""
Initalise a new portfolio with a given balance of one or more currency
"""


class Portfolio:
    def __init__(self) -> None:
        ...

    def create_portfolio(self, username: str, currencies: dict[str, float]) -> None:
        """
        Create new portfolio user in portfolio table and add currencies to portfolio_balance table
        """
        create_new_portfolio_user(username=username)
        add_balances_to_portfolio_balance_table(
            username=username, currencies=currencies
        )
        return

    def update_portfolio_balance(self, username: str, currencies: dict[str, float]):
        """
        Update currencies in portflio_balance for user (username)
        """
        add_balances_to_portfolio_balance_table(
            username=username, currencies=currencies
        )

    def get_balance(self, username: str) -> dict:
        ...


# p = Portfolio().create_portfolio(username="Bianca", currencies={
#     'GBP': 200.0,
# })

# p2 = Portfolio().update_portfolio_balance(username="Bianca", currencies={
#     'GBP': 200.0,
# })
