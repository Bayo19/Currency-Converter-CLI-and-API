from __future__ import annotations
from typing import Optional
from functools import reduce
from db.database_functions import (
    add_balances_to_portfolio_balance_table,
    create_new_portfolio_user,
    user_exists,
    get_portfolio_from_table,
    subtract_amount_from_currency,
    add_amount_to_currency,
)

from convert import FXConverter


class Portfolio:
    def __init__(
        self, username: str, balance: Optional[dict[str, float]] = None
    ) -> None:
        self.username = username
        self.balance = balance
        self.converter = FXConverter()

    def create_portfolio(
        self,
    ) -> None:
        """
        Create new portfolio user in portfolio table and add currencies to portfolio_balance table
        """
        try:
            create_new_portfolio_user(username=self.username)
        except ValueError:
            raise ValueError

        add_balances_to_portfolio_balance_table(
            username=self.username, balance_map=self.balance
        )
        return

    def update_portfolio_balance(self, balance_map: dict[str, float]) -> None:
        """
        Update currencies in portflio_balance for user (username)
        """
        if not user_exists(username=self.username):
            raise ValueError
        add_balances_to_portfolio_balance_table(
            username=self.username, balance_map=balance_map
        )

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
                    convert=current.currency_code,
                    to=base_currency,
                ).converted_amount,
                portfolio_items,
                0,
            )
            return "{:.2f}".format(portfolio_total_value)
        return 0

    def trade_currencies(
        self,
        source_currency_code: str,
        target_currency_code: str,
        source_amount: str,
        other_portfolio_name: str,
    ) -> None:

        source_portfolio = get_portfolio_from_table(username=self.username)
        target_portfolio = get_portfolio_from_table(username=other_portfolio_name)

        target_amount = float(
            self.converter.convert_currency_(
                amount=source_amount,
                convert=source_currency_code,
                to=target_currency_code,
            ).converted_amount
        )

        other_user_has_target_currency = bool(
            [
                t
                for t in target_portfolio
                if t.currency_code == target_currency_code and t.amount >= target_amount
            ]
        )

        source_user_has_source_currency = bool(
            [
                s
                for s in source_portfolio
                if s.currency_code == source_currency_code and s.amount >= source_amount
            ]
        )

        if source_user_has_source_currency and other_user_has_target_currency:
            subtract_amount_from_currency(
                username=self.username,
                currency=source_currency_code,
                amount=source_amount,
            )
            add_amount_to_currency(
                username=other_portfolio_name,
                currency=source_currency_code,
                amount=source_amount,
            )

            subtract_amount_from_currency(
                username=other_portfolio_name,
                currency=target_currency_code,
                amount=target_amount,
            )
            add_amount_to_currency(
                username=self.username,
                currency=target_currency_code,
                amount=target_amount,
            )
        else:
            raise ValueError


