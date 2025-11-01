import datetime

def get_share_price(symbol: str) -> float:
    """Returns fixed prices for test symbols."""
    prices = {
        "AAPL": 150.0,
        "TSLA": 800.0,
        "GOOGL": 2500.0
    }
    return prices.get(symbol, 0.0)

class Account:
    def __init__(self, username: str, initial_deposit: float) -> None:
        """
        Initialize a new account with a username and initial deposit.
        
        Args:
            username (str): The name of the account user.
            initial_deposit (float): The initial amount deposited.
        """
        self.username = username
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.portfolio = {}
        self.transactions = []
        
        # Record the initial deposit as a transaction
        self.transactions.append({
            "type": "deposit",
            "amount": initial_deposit,
            "timestamp": datetime.datetime.now()
        })
        
    def deposit(self, amount: float) -> None:
        """
        Deposit funds into the account.
        
        Args:
            amount (float): The amount to deposit.
        """
        self.balance += amount
        self.transactions.append({
            "type": "deposit",
            "amount": amount,
            "timestamp": datetime.datetime.now()
        })
        
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw funds from the account if sufficient balance exists.
        
        Args:
            amount (float): The amount to withdraw.
            
        Returns:
            bool: True if withdrawal successful, False otherwise.
        """
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append({
                "type": "withdraw",
                "amount": amount,
                "timestamp": datetime.datetime.now()
            })
            return True
        return False
    
    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """
        Buy shares if sufficient funds are available.
        
        Args:
            symbol (str): The stock symbol.
            quantity (int): The number of shares to buy.
            
        Returns:
            bool: True if purchase successful, False otherwise.
        """
        price = get_share_price(symbol)
        total_cost = price * quantity
        
        if self.balance >= total_cost:
            self.balance -= total_cost
            
            # Update portfolio
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
                
            # Record transaction
            self.transactions.append({
                "type": "buy",
                "symbol": symbol,
                "amount": quantity,
                "price": price,
                "timestamp": datetime.datetime.now()
            })
            return True
        return False
    
    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """
        Sell shares if the user owns enough of them.
        
        Args:
            symbol (str): The stock symbol.
            quantity (int): The number of shares to sell.
            
        Returns:
            bool: True if sale successful, False otherwise.
        """
        if symbol in self.portfolio and self.portfolio[symbol] >= quantity:
            price = get_share_price(symbol)
            sale_value = price * quantity
            
            # Update portfolio
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
                
            # Update balance
            self.balance += sale_value
            
            # Record transaction
            self.transactions.append({
                "type": "sell",
                "symbol": symbol,
                "amount": quantity,
                "price": price,
                "timestamp": datetime.datetime.now()
            })
            return True
        return False
    
    def calculate_portfolio_value(self) -> float:
        """
        Calculate the total value of the portfolio.
        
        Returns:
            float: The total value of all shares in the portfolio.
        """
        total_value = 0.0
        for symbol, quantity in self.portfolio.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        return total_value
    
    def report_holdings(self) -> dict:
        """
        Report the current holdings.
        
        Returns:
            dict: A copy of the portfolio dictionary.
        """
        return self.portfolio.copy()
    
    def report_profit_or_loss(self) -> float:
        """
        Calculate profit or loss from the initial deposit.
        
        Returns:
            float: The profit or loss amount.
        """
        total_value = self.balance + self.calculate_portfolio_value()
        return total_value - self.initial_deposit
    
    def list_transactions(self) -> list:
        """
        List all transactions.
        
        Returns:
            list: A copy of the transactions list.
        """
        return self.transactions.copy()