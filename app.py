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
dividend_rate = ticker.info['dividendRate']
st.write(f"The current price of {stock_symbol} is: ${current_price}")
st.write(f"The current Market cap of {stock_symbol} is: ${market_cap}")
st.write(f"The Dividend Rate of {stock_symbol} is: ${dividend_rate}")