#!/usr/bin/env python
# src/financial_researcher/order_history.py
"""
Order history tracking system for SPX trading agents
Maintains a record of all trades to inform future decisions
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class OrderHistory:
    """Manages order history for SPX options trading"""
    
    def __init__(self, history_file: str = "output/order_history.json"):
        self.history_file = history_file
        self.orders = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load order history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save order history to file"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.orders, f, indent=2)
    
    def add_order(self, 
                  agent_type: str,
                  decision: str,
                  strike_price: float,
                  entry_price: float,
                  expiration: str,
                  reasoning: str,
                  spx_price: float):
        """Add a new order to history"""
        order = {
            "order_id": len(self.orders) + 1,
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,  # "aggressive" or "cautious"
            "decision": decision,  # "CALL" or "PUT"
            "strike_price": strike_price,
            "entry_price": entry_price,
            "spx_price_at_entry": spx_price,
            "expiration": expiration,
            "reasoning": reasoning,
            "status": "OPEN",
            "exit_price": None,
            "profit_loss": None,
            "closed_at": None
        }
        self.orders.append(order)
        self._save_history()
        return order["order_id"]
    
    def close_order(self, 
                    order_id: int, 
                    exit_price: float, 
                    profit_loss: float):
        """Close an existing order"""
        for order in self.orders:
            if order["order_id"] == order_id:
                order["status"] = "CLOSED"
                order["exit_price"] = exit_price
                order["profit_loss"] = profit_loss
                order["closed_at"] = datetime.now().isoformat()
                self._save_history()
                return True
        return False
    
    def get_agent_history(self, agent_type: str) -> List[Dict]:
        """Get order history for a specific agent"""
        return [o for o in self.orders if o["agent_type"] == agent_type]
    
    def get_open_orders(self, agent_type: Optional[str] = None) -> List[Dict]:
        """Get all open orders, optionally filtered by agent"""
        open_orders = [o for o in self.orders if o["status"] == "OPEN"]
        if agent_type:
            open_orders = [o for o in open_orders if o["agent_type"] == agent_type]
        return open_orders
    
    def get_closed_orders(self, agent_type: Optional[str] = None) -> List[Dict]:
        """Get all closed orders, optionally filtered by agent"""
        closed_orders = [o for o in self.orders if o["status"] == "CLOSED"]
        if agent_type:
            closed_orders = [o for o in closed_orders if o["agent_type"] == agent_type]
        return closed_orders
    
    def get_performance_summary(self, agent_type: str) -> Dict:
        """Get performance statistics for an agent"""
        closed = self.get_closed_orders(agent_type)
        
        if not closed:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "total_profit": 0,
                "avg_profit": 0,
                "max_profit": 0,
                "max_loss": 0
            }
        
        profits = [o["profit_loss"] for o in closed]
        winning = [p for p in profits if p > 0]
        losing = [p for p in profits if p < 0]
        
        return {
            "total_trades": len(closed),
            "winning_trades": len(winning),
            "losing_trades": len(losing),
            "win_rate": len(winning) / len(closed) * 100 if closed else 0,
            "total_profit": sum(profits),
            "avg_profit": sum(profits) / len(profits) if profits else 0,
            "max_profit": max(profits) if profits else 0,
            "max_loss": min(profits) if profits else 0
        }
    
    def format_history_for_agent(self, agent_type: str) -> str:
        """Format order history as text for agent context"""
        history = self.get_agent_history(agent_type)
        performance = self.get_performance_summary(agent_type)
        
        output = f"\n=== ORDER HISTORY FOR {agent_type.upper()} TRADER ===\n\n"
        
        # Performance summary
        output += "PERFORMANCE SUMMARY:\n"
        output += f"- Total Trades: {performance['total_trades']}\n"
        output += f"- Win Rate: {performance['win_rate']:.1f}%\n"
        output += f"- Total Profit/Loss: ${performance['total_profit']:.2f}\n"
        output += f"- Average Per Trade: ${performance['avg_profit']:.2f}\n"
        output += f"- Best Trade: ${performance['max_profit']:.2f}\n"
        output += f"- Worst Trade: ${performance['max_loss']:.2f}\n\n"
        
        # Open positions
        open_orders = self.get_open_orders(agent_type)
        if open_orders:
            output += f"OPEN POSITIONS ({len(open_orders)}):\n"
            for order in open_orders[-5:]:  # Last 5 open
                output += f"- Order #{order['order_id']}: {order['decision']} {order['strike_price']} "
                output += f"@ ${order['entry_price']:.2f} (Exp: {order['expiration']})\n"
            output += "\n"
        
        # Recent closed trades
        closed_orders = self.get_closed_orders(agent_type)
        if closed_orders:
            output += f"RECENT CLOSED TRADES (Last 10):\n"
            for order in closed_orders[-10:]:
                pl_sign = "+" if order['profit_loss'] > 0 else ""
                output += f"- Order #{order['order_id']}: {order['decision']} {order['strike_price']} "
                output += f"- Entry: ${order['entry_price']:.2f}, Exit: ${order['exit_price']:.2f} "
                output += f"- P/L: {pl_sign}${order['profit_loss']:.2f}\n"
        
        return output
    
    def get_all_orders(self) -> List[Dict]:
        """Get all orders"""
        return self.orders

