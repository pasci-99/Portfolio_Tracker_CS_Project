import streamlit as st
import yfinance as yf
import pandas as pd

# Function to format camelCase names into a readable format
def format_camel_case(name):
    formatted_name = ''.join([' ' + char if char.isupper() else char for char in name]).strip()
    return formatted_name.title()

# Function to fetch stock data
def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

# Fetch data for a sample stock to get all data points
sample_stock = yf.Ticker('AAPL')
sample_data = sample_stock.info

# Extract and format all available data points
all_data_points = [format_camel_case(point) for point in sample_data.keys()]

# Multiselect dropdown for choosing data points
selected_data_points = st.multiselect('Select data points for comparison', all_data_points, default=['Current Price', 'Market Cap'])

# Function to get the original key from formatted name
def get_original_key(formatted_name):
    for key in sample_data.keys():
        if format_camel_case(key) == formatted_name:
            return key
    return None

# Input fields for stock symbols
stock1 = st.text_input('Enter first stock symbol', 'AAPL')
stock2 = st.text_input('Enter second stock symbol', 'NVDA')

# Fetch data for entered symbols
data_stock1 = fetch_stock_data(stock1) if stock1 else None
data_stock2 = fetch_stock_data(stock2) if stock2 else None

# Only proceed if both stocks have been entered
if data_stock1 and data_stock2:
    # Adjust the data fetching to use the original keys
    comparison_data = {
        'Data Point': selected_data_points,
        stock1: [data_stock1.get(get_original_key(point)) for point in selected_data_points],
        stock2: [data_stock2.get(get_original_key(point)) for point in selected_data_points]
    }

    # Create and display the DataFrame
    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)
