from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Earnings, StockSplit
from datetime import datetime, timedelta
from surmount.utils import is_market_open, get_next_weekday

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["TSLA"]
        self.data_list = [
            Earnings("TSLA"),
            StockSplit("AAPL"),  # Assuming Magnificent 7 checks can be generalized or specifically listed.
            StockSplit("GOOGL"), # Repeat for others in Magnificent 7.
            StockSplit("NVDA"),
            StockSplit("MSFT"),
            StockSplit("AMZN"),
            StockSplit("META")
            # More StockSplit instances as needed...
        ]
        self.current_date = None
        self.option_strike_distance = 10  # $10 from current price condition.

    @property
    def interval(self):
        return "1min"  # The finest granularity given the task requirements.

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        if not self.is_right_timing():
            return TargetAllocation({})

        if self.has_earnings_next_week("TSLA") or not self.is_full_trading_week() or self.recent_stock_split():
            return TargetAllocation({})

        option_price_check = self.check_option_prices("TSLA", self.option_strike_distance)
        if option_price_check:
            allocation = {"TSLA Straddle": 1}  # Pseudocode, as actual option trading specifics depend on external factors.
        else:
            allocation = {}
        
        return TargetAllocation(allocation)

    def is_right_timing(self):
        # Check if current time is 1 minute before market close on Friday.
        now = datetime.now()
        if now.weekday() == 4 and is_market_open(now) and (now.hour, now.minute) >= (15, 59):  # Assuming NYSE timings.
            return True
        return False

    def has_earnings_next_week(self, ticker):
        # Should check Earnings data for the ticker and verify if earnings are reported next week.
        # Placeholder, assuming function implementation exists.
        pass

    def is_full_trading_week(self):
        # Check if the next week has 5 trading days (no holidays).
        # Placeholder, implementation depends on trading calendar.
        pass

    def recent_stock_split(self):
        # Check if any of the Magnificent 7 stocks have announced an upcoming split in the past 3 weeks.
        # Placeholder, assuming function implementation exists.
        pass

    def check_option_prices(self, ticker, strike_distance):
        # Check if TSLA's put and call option prices are at least $10 away from the current price.
        # This requires querying option chain data, which typically involves external APIs.
        # Placeholder, assuming function implementation exists.
        pass