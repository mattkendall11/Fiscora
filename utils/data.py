import numpy as np

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