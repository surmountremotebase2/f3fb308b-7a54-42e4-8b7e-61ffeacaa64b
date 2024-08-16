from surmount.base_class import Strategy, TargetAllocation
from datetime import datetime, timedelta

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TSLA"]  # Target TSLA for the strategy

    @property
    def assets(self):
        return self.tickers
    
    @property
    def interval(self):
        # Assuming the closest available interval is "1min" for checking price close to market close
        return "1min"

    def run(self, data):
        # Initial allocation - By default, do not allocate (this part of the code needs to execute trading logic outside the Surmount framework)
        allocation_dict = {"TSLA": 0}
        
        # Check if current time is five minutes before the market close on a Friday
        current_time = datetime.now()
        # Market close time is typically 16:00, so we're aiming for 15:55 on a Friday
        # NOTE: This example assumes the system is in the same timezone as the market
        if current_time.weekday() == 4 and current_time.hour == 15 and current_time.minute == 55:
            # This is the place where the logic for initiating a long strangle option strategy would be called
            # However, the actual purchase of options and setting the strike prices would need to be handled externally or through a more advanced capability of Surmount not covered here
            
            # Log or notify that this is the strategic point to initiate the options strategy
            print("Execute long strangle options strategy on TSLA.")
        
        # Return allocation - in a real application this might trigger or signal an external system to execute the options trades
        return TargetAllocation(allocation_dict)