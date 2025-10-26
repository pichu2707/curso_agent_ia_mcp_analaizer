import unittest
from unittest.mock import patch
from accounts import get_share_price, Account

class TestGetSharePrice(unittest.TestCase):
    def test_known_symbols(self):
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("TSLA"), 700.0)
        self.assertEqual(get_share_price("GOOGL"), 2800.0)
    
    def test_unknown_symbol(self):
        self.assertEqual(get_share_price("UNKNOWN"), 0.0)

class TestAccount(unittest.TestCase):
    def setUp(self):
        # This will run before each test
        self.account = Account("user123", 1000.0)
    
    def test_initialization(self):
        self.assertEqual(self.account.user_id, "user123")
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.positions, {})
        self.assertEqual(self.account.transactions, [])
    
    def test_deposit_valid(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
    
    def test_deposit_invalid(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)
    
    def test_withdraw_valid(self):
        self.account.withdraw(500.0)
        self.assertEqual(self.account.balance, 500.0)
    
    def test_withdraw_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0.0)
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.0)
    
    def test_withdraw_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1500.0)
    
    @patch("accounts.get_share_price")
    def test_buy_stock(self, mock_get_share_price):
        # Mock get_share_price to return 50.0
        mock_get_share_price.return_value = 50.0
        
        self.account.buy_stock("XYZ", 10)
        
        # Check if balance is updated correctly
        self.assertEqual(self.account.balance, 500.0)  # 1000 - (50*10)
        
        # Check if positions are updated correctly
        self.assertEqual(self.account.positions, {"XYZ": 10})
        
        # Check if transactions are updated correctly
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], ("BUY", "XYZ", 10, 50.0, 500.0))
    
    @patch("accounts.get_share_price")
    def test_buy_stock_insufficient_funds(self, mock_get_share_price):
        # Mock get_share_price to return 200.0
        mock_get_share_price.return_value = 200.0
        
        with self.assertRaises(ValueError):
            self.account.buy_stock("XYZ", 6)  # 200*6 > 1000
    
    @patch("accounts.get_share_price")
    def test_sell_stock(self, mock_get_share_price):
        # First buy some stock
        mock_get_share_price.return_value = 50.0
        self.account.buy_stock("XYZ", 10)  # Balance becomes 500.0
        
        # Then sell some of it
        mock_get_share_price.return_value = 60.0  # Price went up
        self.account.sell_stock("XYZ", 5)
        
        # Check if balance is updated correctly
        self.assertEqual(self.account.balance, 800.0)  # 500 + (60*5)
        
        # Check if positions are updated correctly
        self.assertEqual(self.account.positions, {"XYZ": 5})
        
        # Check if transactions are updated correctly
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1], ("SELL", "XYZ", 5, 60.0, 300.0))
    
    @patch("accounts.get_share_price")
    def test_sell_stock_complete_position(self, mock_get_share_price):
        # First buy some stock
        mock_get_share_price.return_value = 50.0
        self.account.buy_stock("XYZ", 10)  # Balance becomes 500.0
        
        # Then sell all of it
        mock_get_share_price.return_value = 60.0  # Price went up
        self.account.sell_stock("XYZ", 10)
        
        # Check if position is removed
        self.assertNotIn("XYZ", self.account.positions)
    
    def test_sell_stock_insufficient_shares(self):
        with self.assertRaises(ValueError):
            self.account.sell_stock("XYZ", 5)  # Don't own any XYZ
        
        # Buy some but not enough
        with patch("accounts.get_share_price", return_value=50.0):
            self.account.buy_stock("XYZ", 3)
        
        with self.assertRaises(ValueError):
            self.account.sell_stock("XYZ", 5)  # Only own 3 XYZ
    
    @patch("accounts.get_share_price")
    def test_get_portfolio_value(self, mock_get_share_price):
        # Mock to return different values based on symbol
        def side_effect(symbol):
            return {"ABC": 100.0, "XYZ": 50.0}.get(symbol, 0.0)
        
        mock_get_share_price.side_effect = side_effect
        
        # Buy some stocks
        self.account.positions = {"ABC": 5, "XYZ": 10}
        self.account.balance = 500.0
        
        # Calculate expected portfolio value
        expected_value = 500.0 + (5 * 100.0) + (10 * 50.0)
        self.assertEqual(self.account.get_portfolio_value(), expected_value)
    
    @patch("accounts.get_share_price")
    def test_get_profit_loss(self, mock_get_share_price):
        # Mock to return 200.0 for any symbol
        mock_get_share_price.return_value = 200.0
        
        # Buy some stocks
        self.account.positions = {"ABC": 5}
        self.account.balance = 500.0
        
        # Calculate expected profit/loss
        expected_profit_loss = (500.0 + (5 * 200.0)) - 1000.0
        self.assertEqual(self.account.get_profit_loss(), expected_profit_loss)
    
    def test_get_holdings(self):
        self.account.positions = {"ABC": 5, "XYZ": 10}
        self.assertEqual(self.account.get_holdings(), {"ABC": 5, "XYZ": 10})
    
    def test_get_transactions(self):
        transactions = [("BUY", "ABC", 5, 100.0, 500.0), ("SELL", "ABC", 2, 120.0, 240.0)]
        self.account.transactions = transactions
        self.assertEqual(self.account.get_transactions(), transactions)

if __name__ == "__main__":
    unittest.main()