from datetime import datetime, timedelta
from src.pricer import get_option_price
import pandas as pd

# Example usage
if __name__ == "__main__":
    # Example parameters
    ticker = "AAPL"
    strike = 180.0
    expiry = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    # Calculate both call and put options
    call_price = get_option_price(ticker, strike, expiry, 'call')
    put_price = get_option_price(ticker, strike, expiry, 'put')

    print("\nCall Option:")
    print(pd.DataFrame([call_price]).to_string(index=False))
    print("\nPut Option:")
    print(pd.DataFrame([put_price]).to_string(index=False))


