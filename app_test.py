import streamlit as st
import yfinance as yf
import pandas as pd


# Fetch data for a sample stock
sample_stock = yf.Ticker('AAPL')
sample_data = sample_stock.info

# Extract all available data points
all_data_points = list(sample_data.keys())


# Multiselect dropdown for choosing data points
selected_data_points = st.multiselect('Select data points for comparison', all_data_points, default=['currentPrice', 'marketCap'])


# Function to fetch data for a given stock
def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

# Input fields for stock symbols
stock1 = st.text_input('Enter first stock symbol', 'AAPL')
stock2 = st.text_input('Enter second stock symbol', 'NVDA')

# Fetch data for entered symbols
data_stock1 = fetch_stock_data(stock1)
data_stock2 = fetch_stock_data(stock2)

# Creating a DataFrame for the comparison table
comparison_data = {
    'Data Point': selected_data_points,
    stock1: [data_stock1.get(point) for point in selected_data_points],
    stock2: [data_stock2.get(point) for point in selected_data_points]
}

comparison_df = pd.DataFrame(comparison_data)

# Display the DataFrame as a table in Streamlit
st.table(comparison_df)
