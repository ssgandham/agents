import unittest
from unittest.mock import patch, MagicMock
import datetime
from accounts import Account, get_share_price


class TestGetSharePrice(unittest.TestCase):
    def test_get_existing_share_price(self):
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("TSLA"), 800.0)
        self.assertEqual(get_share_price("GOOGL"), 2500.0)
        
    def test_get_nonexistent_share_price(self):
        self.assertEqual(get_share_price("NONEXISTENT"), 0.0)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("testuser", 1000.0)

    def test_init(self):
        self.assertEqual(self.account.username, "testuser")
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]["type"], "deposit")
        self.assertEqual(self.account.transactions[0]["amount"], 1000.0)

    def test_deposit(self):
        initial_balance = self.account.balance
        initial_transactions_count = len(self.account.transactions)
        
        self.account.deposit(500.0)
        
        self.assertEqual(self.account.balance, initial_balance + 500.0)
        self.assertEqual(len(self.account.transactions), initial_transactions_count + 1)
        self.assertEqual(self.account.transactions[-1]["type"], "deposit")
        self.assertEqual(self.account.transactions[-1]["amount"], 500.0)

    def test_withdraw_sufficient_funds(self):
        initial_balance = self.account.balance
        initial_transactions_count = len(self.account.transactions)
        
        result = self.account.withdraw(500.0)
        
        self.assertTrue(result)
        self.assertEqual(self.account.balance, initial_balance - 500.0)
        self.assertEqual(len(self.account.transactions), initial_transactions_count + 1)
        self.assertEqual(self.account.transactions[-1]["type"], "withdraw")
        self.assertEqual(self.account.transactions[-1]["amount"], 500.0)

    def test_withdraw_insufficient_funds(self):
        initial_balance = self.account.balance
        initial_transactions_count = len(self.account.transactions)
        
        result = self.account.withdraw(2000.0)  # More than balance
        
        self.assertFalse(result)
        self.assertEqual(self.account.balance, initial_balance)  # Balance unchanged
        self.assertEqual(len(self.account.transactions), initial_transactions_count)  # No new transaction

    def test_buy_shares_sufficient_funds(self):
        initial_balance = self.account.balance
        initial_transactions_count = len(self.account.transactions)
        
        result = self.account.buy_shares("AAPL", 2)  # 2 shares at $150 each = $300
        
        self.assertTrue(result)
        self.assertEqual(self.account.balance, initial_balance - 300.0)
        self.assertEqual(self.account.portfolio.get("AAPL"), 2)
        self.assertEqual(len(self.account.transactions), initial_transactions_count + 1)
        self.assertEqual(self.account.transactions[-1]["type"], "buy")
        self.assertEqual(self.account.transactions[-1]["symbol"], "AAPL")
        self.assertEqual(self.account.transactions[-1]["amount"], 2)
        self.assertEqual(self.account.transactions[-1]["price"], 150.0)

    def test_buy_shares_insufficient_funds(self):
        initial_balance = self.account.balance
        initial_transactions_count = len(self.account.transactions)
        
        # Try to buy shares worth more than balance
        result = self.account.buy_shares("GOOGL", 1)  # 1 share at $2500 > $1000 balance
        
        self.assertFalse(result)
        self.assertEqual(self.account.balance, initial_balance)  # Balance unchanged
        self.assertNotIn("GOOGL", self.account.portfolio)  # No shares added
        self.assertEqual(len(self.account.transactions), initial_transactions_count)  # No new transaction

    def test_buy_more_of_existing_shares(self):
        # First buy
        self.account.buy_shares("AAPL", 2)
        initial_shares = self.account.portfolio["AAPL"]
        
        # Buy more
        self.account.buy_shares("AAPL", 3)
        
        self.assertEqual(self.account.portfolio["AAPL"], initial_shares + 3)

    def test_sell_shares_sufficient_shares(self):
        # Buy shares first
        self.account.buy_shares("AAPL", 5)
        initial_balance = self.account.balance
        initial_transactions_count = len(self.account.transactions)
        
        # Sell some
        result = self.account.sell_shares("AAPL", 2)
        
        self.assertTrue(result)
        self.assertEqual(self.account.portfolio["AAPL"], 3)  # 5 - 2 = 3
        self.assertEqual(self.account.balance, initial_balance + (150.0 * 2))  # Added 2 shares * $150
        self.assertEqual(len(self.account.transactions), initial_transactions_count + 1)
        self.assertEqual(self.account.transactions[-1]["type"], "sell")
        self.assertEqual(self.account.transactions[-1]["symbol"], "AAPL")
        self.assertEqual(self.account.transactions[-1]["amount"], 2)
        self.assertEqual(self.account.transactions[-1]["price"], 150.0)

    def test_sell_all_shares(self):
        # Buy shares first
        self.account.buy_shares("AAPL", 2)
        
        # Sell all
        result = self.account.sell_shares("AAPL", 2)
        
        self.assertTrue(result)
        self.assertNotIn("AAPL", self.account.portfolio)  # Key should be removed when no shares left

    def test_sell_shares_insufficient_shares(self):
        # Buy some shares
        self.account.buy_shares("AAPL", 2)
        initial_balance = self.account.balance
        initial_portfolio = self.account.portfolio.copy()
        initial_transactions_count = len(self.account.transactions)
        
        # Try to sell more than owned
        result = self.account.sell_shares("AAPL", 5)  # Only have 2
        
        self.assertFalse(result)
        self.assertEqual(self.account.balance, initial_balance)  # Balance unchanged
        self.assertEqual(self.account.portfolio, initial_portfolio)  # Portfolio unchanged
        self.assertEqual(len(self.account.transactions), initial_transactions_count)  # No new transaction

    def test_sell_shares_nonexistent_symbol(self):
        initial_balance = self.account.balance
        initial_transactions_count = len(self.account.transactions)
        
        result = self.account.sell_shares("NONEXISTENT", 1)
        
        self.assertFalse(result)
        self.assertEqual(self.account.balance, initial_balance)  # Balance unchanged
        self.assertEqual(len(self.account.transactions), initial_transactions_count)  # No new transaction

    def test_calculate_portfolio_value_empty(self):
        value = self.account.calculate_portfolio_value()
        self.assertEqual(value, 0.0)

    def test_calculate_portfolio_value(self):
        # Buy some shares
        self.account.buy_shares("AAPL", 2)  # 2 * $150 = $300
        self.account.buy_shares("TSLA", 1)  # 1 * $800 = $800
        
        value = self.account.calculate_portfolio_value()
        self.assertEqual(value, 300.0 + 800.0)

    def test_report_holdings_empty(self):
        holdings = self.account.report_holdings()
        self.assertEqual(holdings, {})
        
        # Ensure it's a copy, not the original
        holdings["TEST"] = 1
        self.assertNotIn("TEST", self.account.portfolio)

    def test_report_holdings(self):
        # Buy some shares
        self.account.buy_shares("AAPL", 2)
        self.account.buy_shares("TSLA", 1)
        
        holdings = self.account.report_holdings()
        
        self.assertEqual(holdings, {"AAPL": 2, "TSLA": 1})
        
        # Ensure it's a copy, not the original
        holdings["AAPL"] = 10
        self.assertEqual(self.account.portfolio["AAPL"], 2)  # Original unchanged

    def test_report_profit_or_loss_no_change(self):
        # No trades yet, just initial deposit
        profit_loss = self.account.report_profit_or_loss()
        self.assertEqual(profit_loss, 0.0)  # No profit/loss yet

    def test_report_profit_or_loss_with_holdings(self):
        # Buy some shares
        self.account.buy_shares("AAPL", 2)  # 2 * $150 = $300
        # Balance is now $700, portfolio value is $300
        
        profit_loss = self.account.report_profit_or_loss()
        
        # Total value is still $1000, so profit/loss = 0
        self.assertEqual(profit_loss, 0.0)
        
    def test_report_profit_or_loss_with_profit(self):
        # Simulate a scenario where share price increases after purchase
        self.account.buy_shares("AAPL", 2)  # 2 shares at $150 = $300
        
        # Mock the get_share_price to return a higher price for AAPL
        with patch('accounts.get_share_price') as mock_price:
            mock_price.return_value = 200.0  # Price increased to $200
            
            # Now our shares are worth 2 * $200 = $400 (a $100 profit)
            profit_loss = self.account.report_profit_or_loss()
            
            # Original balance ($1000) - spent ($300) + current portfolio value ($400) - initial deposit ($1000) = $100
            self.assertEqual(profit_loss, 100.0)

    def test_list_transactions(self):
        initial_transactions = self.account.list_transactions()
        
        # Should have 1 initial deposit transaction
        self.assertEqual(len(initial_transactions), 1)
        self.assertEqual(initial_transactions[0]["type"], "deposit")
        
        # Add more transactions
        self.account.deposit(200.0)
        self.account.withdraw(100.0)
        self.account.buy_shares("AAPL", 1)
        
        transactions = self.account.list_transactions()
        
        self.assertEqual(len(transactions), 4)  # 1 initial + 3 new
        self.assertEqual(transactions[1]["type"], "deposit")
        self.assertEqual(transactions[1]["amount"], 200.0)
        self.assertEqual(transactions[2]["type"], "withdraw")
        self.assertEqual(transactions[2]["amount"], 100.0)
        self.assertEqual(transactions[3]["type"], "buy")
        self.assertEqual(transactions[3]["symbol"], "AAPL")
        
        # Ensure it's a copy, not the original
        original_transaction_count = len(transactions)
        transactions.append({"fake": "transaction"})
        self.assertEqual(len(self.account.transactions), original_transaction_count)  # Original unchanged


if __name__ == '__main__':
    unittest.main()