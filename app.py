pip install yfinance

import streamlit as st
import yfinance as yf
import pandas as pd

st.write("Hooray, we connected everything")

st.write("Test")

# Function to fetch stock data using yfinance
def get_stock_data(symbol, interval='1d'):
    stock = yf.Ticker(symbol)
    data = stock.history(period=interval)
    return data

# Streamlit app
st.title("Stock Price Viewer")

# Sidebar for user input
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL):", "AAPL")
interval = st.sidebar.selectbox("Select Time Interval:", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])

# Fetch and display stock data
stock_data = get_stock_data(symbol, interval)
if stock_data is not None:
    st.write(f"Stock Price Data for {symbol}")
    st.line_chart(stock_data['Close'])