from portfolio.data_fetcher import DataFetcher

class PortfolioManager:
    def __init__(self):
        self.data_fethcer = DataFetcher()
        self.portfolio = {}

    def add_asset(self, symbol, quantity):
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity

    def remove_asset(self, symbol, quantity):
        if symbol in self.portfolio:
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] <= 0: del self.portfolio[symbol]
    

    def get_portfolio_value(self):
        total_val = 0 
        for symbol, qty in self.portfolio.items():
            price  = self.data_fethcer.get_price(symbol)
            total_val += qty * price
        return total_val
    

    def show_portfolio(self):
        print("\Current Portfolio Value:")
        for symbol, qty in self.portfolio.items():
            price  = self.data_fethcer.get_price(symbol)  
            value = qty * price
            print(f"{symbol}: {qty} units @ ${price:.2f} = ${value:.2f}")
            print(f"\nTotal Value: ${self.get_portfolio_value():.2f}\n")



