import yfinance as yf
import os
import time
import pandas as pd
from yahoo_fin.stock_info import get_data

#get data
amazon_weekly= get_data("amzn", start_date="12/04/2009", end_date="12/04/2019", index_as_date = True, interval="1wk")
print(type(amazon_weekly))

# Define a timing decorator
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken by {func.__name__}: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@timing_decorator
def read_data(token):
    token_data = yf.Ticker(token)
    return token_data.history(start="2024-06-02", end="2025-01-05", interval="1d")

msft_data =  yf.download("MSFT", period="5y")  # Adjust the period as needed
tempus = yf.download("TEM", period="5y")
print(tempus.info)
print(msft_data.info)



read_data("aapl")
read_data("amzn")

tickers = ["AAPL", "MSFT", "GOOG"]  # Add your thousands of tickers here
#Download and save data
def download_historical_data(tickers):
    output_dir = "historical_data"
    os.makedirs(output_dir, exist_ok=True)
    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        try:
            # Fetch historical data
            data = yf.download(ticker, period="5y")  # Adjust the period as needed

            # Save to CSV
            file_path = os.path.join(output_dir, f"{ticker}.csv")
            data.to_csv(file_path)
            time.sleep(0.5)
            print(f"Data for {ticker} saved to {file_path}")
        except Exception as e:
            print(f"Failed to download data for {ticker}: {e}")

def download_fundamental_data(tickers):
    output_dir_cashflow = "cashflow"
    output_dir_balancesheet = "balancesheet"
    output_dir_financial = "financial"
    os.makedirs(output_dir_cashflow, exist_ok=True)
    os.makedirs(output_dir_balancesheet, exist_ok=True)
    os.makedirs(output_dir_financial, exist_ok=True)

    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        try:
            # Fetch historical data
            data = yf.Ticker(ticker)

            # Save to CSV
            data_cashflow = data.cashflow
            data_financial = data.financials
            data_balancesheet = data.balancesheet
            cashflow_file_path = os.path.join(output_dir_cashflow, f"{ticker}_cashflow.csv")
            financial_file_path = os.path.join(output_dir_financial, f"{ticker}_financial.csv")
            balancesheet_file_path = os.path.join(output_dir_balancesheet, f"{ticker}_balancesheet.csv")
            data_cashflow.to_csv(cashflow_file_path)
            data_financial.to_csv(financial_file_path)
            data_balancesheet.to_csv(balancesheet_file_path)
        except Exception as e:
            print(f"Failed to download data for {ticker}: {e}")


nasdaq_stocks = pd.read_csv("nasdaq.csv")
symbol_list = nasdaq_stocks["Symbol"].tolist()

download_historical_data(symbol_list)
