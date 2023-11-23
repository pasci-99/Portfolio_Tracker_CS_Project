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


import yfinance as yf

# Function to fetch stock data
def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

# Fetch data for entered symbols
data_stock1 = fetch_stock_data(stock1)
data_stock2 = fetch_stock_data(stock2)

