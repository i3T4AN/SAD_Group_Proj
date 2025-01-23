import yfinance as yf
import pandas as pd
import numpy as np
import time

# Function to fetch stock data from Yahoo Finance with real-time interval
def fetch_real_time_stock_data(ticker, period='1d', interval='1m'):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period=period, interval=interval)
        return stock_data
    except Exception as e:
        print(f"Error fetching real-time data for {ticker}: {e}")
        return None

# Function to calculate key financial metrics
def calculate_metrics(stock_data):
    stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()

    delta = stock_data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))
    
    stock_data['ROI'] = (stock_data['Close'] - stock_data['Close'].shift(1)) / stock_data['Close'].shift(1)
    
    stock_data['P/E'] = np.random.uniform(10, 30, len(stock_data))  # Simulating P/E

    return stock_data

# Function to make stock recommendations based on metrics
def recommend(stock_data):
    last_row = stock_data.iloc[-1]  # Latest data point
    
    if last_row['50_MA'] > last_row['200_MA'] and last_row['RSI'] < 70:
        recommendation = "Buy"
    elif last_row['RSI'] > 70:
        recommendation = "Sell"
    else:
        recommendation = "Hold"
    
    return recommendation

# Function to simulate fake trades
def simulate_fake_trade(starting_cash, stock_data, recommendation):
    last_price = stock_data['Close'].iloc[-1]

    if recommendation == "Buy":
        # Buy as many shares as possible with the available cash
        num_shares = starting_cash // last_price
        remaining_cash = starting_cash - (num_shares * last_price)
        print(f"Fake trade: Based on recommendation '{recommendation}'")
        print(f"Bought {num_shares} shares at ${last_price:.2f}, remaining cash: ${remaining_cash:.2f}")
    elif recommendation == "Sell":
        # Sell all shares
        num_shares = starting_cash // last_price  # Assuming you're holding all shares
        remaining_cash = starting_cash + (num_shares * last_price)
        print(f"Fake trade: Based on recommendation '{recommendation}'")
        print(f"Sold {num_shares} shares at ${last_price:.2f}, total cash: ${remaining_cash:.2f}")
    else:
        # Hold, no transaction occurs
        print(f"Recommendation is '{recommendation}', no action taken.")
        remaining_cash = starting_cash

    return remaining_cash


# Main function to run real-time stock analyzer
def real_time_stock_analyzer(ticker, starting_cash, refresh_interval=60):
    cash_balance = starting_cash  # Initialize with starting cash
    print(f"Starting real-time stock analysis for {ticker}...")

    while True:
        stock_data = fetch_real_time_stock_data(ticker)

        if stock_data is not None:
            stock_data = calculate_metrics(stock_data)

            # Save analyzed data to CSV
            stock_data.to_csv(f'{ticker}_real_time_analyzed_data.csv', index=False)

            # Get recommendation
            recommendation = recommend(stock_data)
            print(f"\nReal-time recommendation for {ticker}: {recommendation}")

            # Simulate fake trade based on the recommendation
            cash_balance = simulate_fake_trade(cash_balance, stock_data, recommendation)

        print(f"Waiting {refresh_interval} seconds for the next update...\n")
        time.sleep(refresh_interval)  # Wait before the next update


# Example usage
if __name__ == "__main__":
    ticker = 'AAPL'  # Example stock ticker
    starting_cash = 10000  # Fake starting cash for trading simulation
    refresh_interval = 60  # Set the data refresh interval to 1 minute
    
    real_time_stock_analyzer(ticker, starting_cash, refresh_interval)
