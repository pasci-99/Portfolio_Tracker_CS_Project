import streamlit as st
import yfinance as yf
import pandas as pd


# enter andd create a stock symbol 
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL):", "AAPL")

# create the ticker with the symbol
ticker = yf.Ticker(stock_symbol)

# get the wanted data from the ticker
current_price = ticker.info['ask']
market_cap = ticker.info['marketCap']
st.table
st.write(f"The current price of {stock_symbol} is: ${current_price}")
st.write(f"The current price of {stock_symbol} is: ${market_cap}")