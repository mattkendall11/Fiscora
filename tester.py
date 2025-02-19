import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from datetime import datetime, timedelta


def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes option price

    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free interest rate
    sigma: Volatility
    option_type: 'call' or 'put'

    Returns:
    option_price: Calculated option price
    """
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put option
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return option_price


def calculate_historical_volatility(stock_data, window=252):
    """
    Calculate historical volatility from stock prices

    Parameters:
    stock_data: DataFrame with stock prices
    window: Number of days to use for volatility calculation (default: 252 trading days)

    Returns:
    volatility: Annualized volatility
    """
    # Calculate daily returns
    returns = np.log(stock_data['Close'] / stock_data['Close'].shift(1))

    # Calculate annualized volatility
    volatility = returns.std() * np.sqrt(252)
    return volatility


def get_option_price(ticker_symbol, strike_price, expiry_date, option_type='call', risk_free_rate=0.05):
    """
    Get option price using Black-Scholes model with data from yfinance

    Parameters:
    ticker_symbol: Stock symbol (e.g., 'AAPL')
    strike_price: Option strike price
    expiry_date: Option expiry date (format: 'YYYY-MM-DD')
    option_type: 'call' or 'put'
    risk_free_rate: Annual risk-free rate (default: 5%)

    Returns:
    dict: Dictionary containing option details and calculated price
    """
    try:
        # Get stock data
        stock = yf.Ticker(ticker_symbol)
        hist_data = stock.history(period='1y')

        if hist_data.empty:
            return f"Error: No data found for {ticker_symbol}"

        # Current stock price
        current_price = hist_data['Close'].iloc[-1]

        # Calculate time to maturity
        expiry = datetime.strptime(expiry_date, '%Y-%m-%d')
        today = datetime.now()
        T = (expiry - today).days / 365

        if T <= 0:
            return "Error: Expiry date must be in the future"

        # Calculate historical volatility
        volatility = calculate_historical_volatility(hist_data)

        # Calculate option price
        option_price = black_scholes(
            S=current_price,
            K=strike_price,
            T=T,
            r=risk_free_rate,
            sigma=volatility,
            option_type=option_type
        )

        return {
            'ticker': ticker_symbol,
            'option_type': option_type,
            'current_price': round(current_price, 2),
            'strike_price': strike_price,
            'days_to_expiry': round(T * 365, 0),
            'volatility': round(volatility * 100, 2),
            'risk_free_rate': round(risk_free_rate * 100, 2),
            'calculated_price': round(option_price, 2)
        }

    except Exception as e:
        return f"Error: {str(e)}"


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


