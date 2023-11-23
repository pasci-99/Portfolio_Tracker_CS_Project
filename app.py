import streamlit as st
import yfinance as yf
import pandas as pd


st.write("Hooray, we connected everything")

st.write("Test")

# Function to get a list of available stock symbols
def get_stock_symbols():
    # Fetch a list of all stock symbols
    all_stock_info = yf.Tickers("AAPL").tickers
    stock_symbols = [info.info['symbol'] for info in all_stock_info]
    return stock_symbols

# Streamlit app
st.title("Stock Selection App")

# Get the list of available stock symbols
all_stock_symbols = get_stock_symbols()

# Create a text input for stock symbol
entered_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):").upper()

# Filter potential stock suggestions based on entered characters
filtered_symbols = [symbol for symbol in all_stock_symbols if entered_symbol in symbol]

# Display the potential stock suggestions in a multiselect widget
selected_symbols = st.multiselect("Select from Potential Stocks:", filtered_symbols)

# Display the selected stock symbols
st.write("Selected Stocks:", selected_symbols)
