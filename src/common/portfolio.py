from __future__ import annotations
from typing import Any
from functools import reduce
from src.db.database_functions import (
    add_balances_to_portfolio_balance_table,
    create_new_portfolio_user,
    user_exists,
    get_portfolio_from_table,
)
from src.common.convert import FXConverter
from src.common.utility_functions import valid_trade, trade
from src.common.custom_exceptions import UserNotFoundError


class Portfolio:
    def __init__(self, username: str) -> None:
        self.username = username
        self.converter = FXConverter()

    def create_portfolio(self, currency_balances: dict[str, float]) -> bool:
        """
        Create new portfolio user in portfolio table and add currencies to portfolio_balance table
        """
        new_user = create_new_portfolio_user(username=self.username)
        if not new_user:
            return False
        add_balances_to_portfolio_balance_table(
            username=self.username, currency_balances=currency_balances
        )
        return True

    def update_portfolio_balance(self, currency_balances: dict[str, float]) -> None:
        """
        Update currencies in portflio_balance for user (username)
        """
        if not user_exists(username=self.username):
            raise UserNotFoundError
        add_balances_to_portfolio_balance_table(
            username=self.username, currency_balances=currency_balances
        )

    def get_portfolio_as_dict(
        self,
    ) -> dict[str, Any]:
        portfolio_items = get_portfolio_from_table(username=self.username)
        if portfolio_items:
            portfolio_as_dict = {
                "user_id": portfolio_items[0].user_id,
                "currencies": {},
                "timestamp": portfolio_items[0].timestamp,
            }

            for p in portfolio_items:
                portfolio_as_dict["currencies"][p.currency_code] = p.amount

            return portfolio_as_dict
        return None

    def get_current_total_portfolio_value(self, base_currency: str = "USD") -> float:
        """
        Retuns the total value of the current portfolio for a user
        """
        portfolio_items = get_portfolio_from_table(username=self.username)
        if portfolio_items:

            portfolio_total_value = reduce(
                lambda accumulator, current: accumulator
                + self.converter.convert_currency_(
                    amount=current.amount,
                    source_currency_code=current.currency_code,
                    target_currency_code=base_currency,
                ).converted_amount,
                portfolio_items,
                0,
            )
            return "{:.2f}".format(portfolio_total_value)
        return 0

    def trade_currencies(
        self,
        buyer_currency_code: str,
        seller_currency_code: str,
        buyer_amount: float,
        seller_portfolio_name: str,
    ) -> bool:

        source_portfolio = get_portfolio_from_table(username=self.username)
        target_portfolio = get_portfolio_from_table(username=seller_portfolio_name)

        if not source_portfolio or not target_portfolio:
            raise ValueError

        seller_amount = float(
            self.converter.convert_currency_(
                amount=buyer_amount,
                source_currency_code=buyer_currency_code,
                target_currency_code=seller_currency_code,
            ).converted_amount
        )

        if valid_trade(
            buyer_portfolio=source_portfolio,
            seller_portfolio=target_portfolio,
            buyer_currency_code=buyer_currency_code,
            seller_currency_code=seller_currency_code,
            buyer_amount=buyer_amount,
            seller_amount=seller_amount,
        ):
            trade(
                buyer_currency_code=buyer_currency_code,
                seller_currency_code=seller_currency_code,
                buyer_amount=buyer_amount,
                seller_amount=seller_amount,
                buyer_username=self.username,
                seller_username=seller_portfolio_name,
            )
            return True
        else:
            return False
