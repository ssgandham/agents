import gradio as gr
import datetime
from accounts import Account, get_share_price

# Global account instance (for demo purposes)
account = None

def create_account(username, initial_deposit):
    global account
    if initial_deposit <= 0:
        return f"Initial deposit must be positive."
    
    account = Account(username, initial_deposit)
    return f"Account created for {username} with an initial deposit of ${initial_deposit:.2f}."

def deposit_funds(amount):
    if account is None:
        return "Please create an account first."
    if amount <= 0:
        return "Deposit amount must be positive."
    
    account.deposit(amount)
    return f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}."

def withdraw_funds(amount):
    if account is None:
        return "Please create an account first."
    if amount <= 0:
        return "Withdrawal amount must be positive."
    
    success = account.withdraw(amount)
    if success:
        return f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}."
    else:
        return f"Insufficient funds. Current balance: ${account.balance:.2f}."

def buy_stock(symbol, quantity):
    if account is None:
        return "Please create an account first."
    if quantity <= 0:
        return "Quantity must be positive."
    
    price = get_share_price(symbol)
    if price == 0.0:
        return f"Invalid symbol: {symbol}. Available: AAPL, TSLA, GOOGL."
    
    total_cost = price * quantity
    if account.balance < total_cost:
        return f"Insufficient funds. Cost: ${total_cost:.2f}, Balance: ${account.balance:.2f}."
    
    success = account.buy_shares(symbol, quantity)
    if success:
        return f"Bought {quantity} shares of {symbol} at ${price:.2f}/share. Total cost: ${total_cost:.2f}. New balance: ${account.balance:.2f}."
    else:
        return "Transaction failed."

def sell_stock(symbol, quantity):
    if account is None:
        return "Please create an account first."
    if quantity <= 0:
        return "Quantity must be positive."
    
    price = get_share_price(symbol)
    if price == 0.0:
        return f"Invalid symbol: {symbol}. Available: AAPL, TSLA, GOOGL."
    
    current_holdings = account.report_holdings().get(symbol, 0)
    if current_holdings < quantity:
        return f"Insufficient shares. You own {current_holdings} shares of {symbol}."
    
    success = account.sell_shares(symbol, quantity)
    if success:
        total_value = price * quantity
        return f"Sold {quantity} shares of {symbol} at ${price:.2f}/share. Total value: ${total_value:.2f}. New balance: ${account.balance:.2f}."
    else:
        return "Transaction failed."

def get_portfolio():
    if account is None:
        return "Please create an account first."
    
    portfolio = account.report_holdings()
    if not portfolio:
        return "No stocks in portfolio."
    
    result = "Current Portfolio:\n"
    total_value = 0
    
    for symbol, quantity in portfolio.items():
        price = get_share_price(symbol)
        value = price * quantity
        total_value += value
        result += f"{symbol}: {quantity} shares at ${price:.2f}/share = ${value:.2f}\n"
    
    result += f"\nTotal portfolio value: ${total_value:.2f}"
    result += f"\nCash balance: ${account.balance:.2f}"
    result += f"\nTotal account value: ${(total_value + account.balance):.2f}"
    return result

def get_profit_loss():
    if account is None:
        return "Please create an account first."
    
    profit_loss = account.report_profit_or_loss()
    return f"Profit/Loss: ${profit_loss:.2f} from initial deposit of ${account.initial_deposit:.2f}"

def get_transactions():
    if account is None:
        return "Please create an account first."
    
    transactions = account.list_transactions()
    if not transactions:
        return "No transactions recorded."
    
    result = "Transaction History:\n"
    for i, t in enumerate(transactions, 1):
        timestamp = t["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        
        if t["type"] == "deposit":
            result += f"{i}. [{timestamp}] Deposit: ${t['amount']:.2f}\n"
        elif t["type"] == "withdraw":
            result += f"{i}. [{timestamp}] Withdraw: ${t['amount']:.2f}\n"
        elif t["type"] == "buy":
            total = t["amount"] * t["price"]
            result += f"{i}. [{timestamp}] Buy: {t['amount']} shares of {t['symbol']} at ${t['price']:.2f}/share. Total: ${total:.2f}\n"
        elif t["type"] == "sell":
            total = t["amount"] * t["price"]
            result += f"{i}. [{timestamp}] Sell: {t['amount']} shares of {t['symbol']} at ${t['price']:.2f}/share. Total: ${total:.2f}\n"
    
    return result

with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Create Account"):
        with gr.Row():
            username_input = gr.Textbox(label="Username")
            initial_deposit_input = gr.Number(label="Initial Deposit", value=1000.0)
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        create_btn.click(create_account, inputs=[username_input, initial_deposit_input], outputs=create_output)
    
    with gr.Tab("Deposit/Withdraw"):
        with gr.Row():
            deposit_input = gr.Number(label="Deposit Amount", value=100.0)
            deposit_btn = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Deposit Result")
        
        with gr.Row():
            withdraw_input = gr.Number(label="Withdraw Amount", value=50.0)
            withdraw_btn = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Withdraw Result")
        
        deposit_btn.click(deposit_funds, inputs=deposit_input, outputs=deposit_output)
        withdraw_btn.click(withdraw_funds, inputs=withdraw_input, outputs=withdraw_output)
    
    with gr.Tab("Buy/Sell Stocks"):
        gr.Markdown("Available Stocks: AAPL, TSLA, GOOGL")
        with gr.Row():
            buy_symbol_input = gr.Textbox(label="Stock Symbol", value="AAPL")
            buy_quantity_input = gr.Number(label="Quantity", value=1, precision=0)
            buy_btn = gr.Button("Buy")
        buy_output = gr.Textbox(label="Buy Result")
        
        with gr.Row():
            sell_symbol_input = gr.Textbox(label="Stock Symbol", value="AAPL")
            sell_quantity_input = gr.Number(label="Quantity", value=1, precision=0)
            sell_btn = gr.Button("Sell")
        sell_output = gr.Textbox(label="Sell Result")
        
        buy_btn.click(buy_stock, inputs=[buy_symbol_input, buy_quantity_input], outputs=buy_output)
        sell_btn.click(sell_stock, inputs=[sell_symbol_input, sell_quantity_input], outputs=sell_output)
    
    with gr.Tab("Portfolio"):
        portfolio_btn = gr.Button("Get Portfolio Status")
        portfolio_output = gr.Textbox(label="Portfolio", lines=10)
        portfolio_btn.click(get_portfolio, inputs=[], outputs=portfolio_output)
        
        profit_loss_btn = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss")
        profit_loss_btn.click(get_profit_loss, inputs=[], outputs=profit_loss_output)
    
    with gr.Tab("Transactions"):
        transactions_btn = gr.Button("View Transaction History")
        transactions_output = gr.Textbox(label="Transactions", lines=15)
        transactions_btn.click(get_transactions, inputs=[], outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()