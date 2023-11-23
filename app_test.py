import streamlit as st
import yfinance as yf
import pandas as pd


# Input fields for stock symbols
stock1 = st.text_input('Enter first stock symbol', 'AAPL')
stock2 = st.text_input('Enter second stock symbol', 'NVDA')

import yfinance as yf

# Function to fetch stock data
def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

# Fetch data for entered symbols
data_stock1 = fetch_stock_data(stock1)
data_stock2 = fetch_stock_data(stock2)


import pandas as pd

# Data points to compare
data_points = ['currentPrice', 'marketCap', 'dividendRate', 'dividendYield']

# Creating a DataFrame for the comparison table
comparison_data = {
    'Data Point': data_points,
    stock1: [data_stock1.get(point) for point in data_points],
    stock2: [data_stock2.get(point) for point in data_points]
}

comparison_df = pd.DataFrame(comparison_data)

# Display the DataFrame as a table in Streamlit
st.table(comparison_df)

