import yfinance as yf
import pandas as pd

def fetch_sp500_tickers():
    # Fetch the S&P 500 tickers for demonstration
    tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    tickers = tables[0]['Symbol'].tolist()
    return tickers

def fetch_data(ticker, expiration_date):
    # Fetch options data
    try:
        opts = yf.Ticker(ticker).option_chain(expiration_date)
        puts = opts.puts

        # Filter out out-of-the-money puts and create an explicit copy
        stock_price = yf.Ticker(ticker).history(period="1d")['Close'][0]
        puts = puts[puts['strike'] < stock_price].copy()
        
        # Add the ETF ticker to the DataFrame
        puts['ETF'] = ticker

        return puts
    except:
        return pd.DataFrame()  # Return an empty dataframe if there's an error

def screener(expiration_date):
    tickers = fetch_sp500_tickers()
    results = []

    for ticker in tickers:
        puts = fetch_data(ticker, expiration_date)
        if not puts.empty:
            results.append(puts)

    # Combine all results
    all_puts = pd.concat(results)
    
    # Determine columns to sort by
    sort_columns = ['ETF', 'strike']
    if 'delta' in all_puts.columns:
        sort_columns.append('delta')
    
    # Sort by determined columns
    all_puts = all_puts.sort_values(by=sort_columns)

    return all_puts

# Example
expiration_date = "2023-09-01"  # Change to your desired expiration date
results = screener(expiration_date)

# Determine which columns to display
display_columns = ['ETF', 'contractSymbol', 'lastPrice', 'strike']
if 'delta' in results.columns:
    display_columns.append('delta')

print(results[display_columns])

