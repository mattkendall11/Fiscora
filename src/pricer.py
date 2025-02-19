import numpy as np
import yfinance as yf
from scipy.stats import norm
import pandas as pd
from datetime import datetime, timedelta
from src.classical import black_scholes
from utils.data import calculate_historical_volatility

def get_option_price(ticker_symbol, strike_price, expiry_date, option_type='call', risk_free_rate=0.05, modeltype = 'BS'):
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
        if modeltype =='BS':
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