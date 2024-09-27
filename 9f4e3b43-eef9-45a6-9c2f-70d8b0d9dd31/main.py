from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, Earnings, NewsHeadline, StockSplit
from surmount.logging import log
from datetime import datetime, timedelta

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "TSLA"
        self.next_week = self.get_next_week_dates()

        self.data_list = [
            Earnings(self.ticker),
            NewsHeadline(self.ticker),
            StockSplit("Magnificent7")  # Assuming "Magnificent7" is a valid identifier for these stocks
        ]
    
    @property
    def interval(self):
        # Use a short interval to check conditions close to market close
        return "1min"
    
    @property
    def assets(self):
        # Focused on TSLA for this strategy
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initialize with no position
        allocation = 0
        
        # Assumptions are made here about how data interfaces work and might need adjustments
        if self.is_near_market_close() and self.is_end_of_week() and not self.tsla_earnings_next_week(data) and not self.magnificent7_stock_split_recent(data) and not self.tsla_ceo_selling_stock(data):
            option_strike_price = self.get_option_strike_price()
            if self.option_price_condition_met(option_strike_price):
                allocation = 1  # Full allocation to the straddle position
        
        return TargetAllocation({self.ticker: allocation})

    def is_near_market_close(self):
        """Assume market closes at 16:00 ET; check if current time is within 1 min before close."""
        now = datetime.now()
        market_close = now.replace(hour=20, minute=0, second=0, microsecond=0)  # Using UTC time
        return now >= (market_close - timedelta(minutes=1)) and now <= market_close

    def is_end_of_week(self):
        """Check if today is the end of the week (Friday)."""
        return datetime.today().weekday() == 4  # Friday

    def tsla_earnings_next_week(self, data):
        """Check if TSLA has earnings reported next week."""
        earnings_dates = data["earnings"]
        for event in earnings_dates:
            if event["date"] in self.next_week:
                return True
        return False

    def magnificent7_stock_split_recent(self, data):
        """Check if a Magnificent 7 stock has reported an upcoming stock split in the past 3 weeks."""
        three_weeks_ago = datetime.now() - timedelta(weeks=3)
        for split in data["stock_splits"]:
            if split["date"] > three_weeks_ago.strftime('%Y-%m-%d'):
                return True
        return False

    def tsla_ceo_selling_stock(self, data):
        """Check if news contains Elon Musk (or TSLA's CEO) selling stock."""
        news = data["news"]
        for article in news:
            if "Elon Musk" in article["content"] and "selling stock" in article["content"]:
                return True
        return False

    def option_price_condition_met(self, strike_price):
        # Placeholder for logic to check option prices relative to current TSLA price
        # Assume a method exists to get current stock price and relevant option prices
        current_price = self.get_current_stock_price("TSLA")
        return abs(current_price - strike_price) >= 10

    def get_next_week_dates(self):
        """Generate dates for the next week to check against earnings announcements."""
        today = datetime.now()
        next_monday = today + timedelta(days=(7 - today.weekday()))
        return [next_monday + timedelta(days=i) for i in range(5)]

    def get_option_strike_price(self):
        # Placeholder for logic to determine the strike price of interest
        return 1000  # Example fixed value

    def get_current_stock_price(self, ticker):
        # Placeholder for obtaining current stock price
        return 800  # Example fixed value