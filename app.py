import streamlit as st
import yfinance as yf
import pandas as pd




# Function to get stock suggestions based on user input
def get_stock_suggestions(query):
    suggestions = yf.Ticker(query).suggestions
    return [s['symbol'] for s in suggestions]

# Streamlit app
def main():
    st.title("Stock Comparison App")

    # User input for stock search
    stock_query = st.text_input("Enter a stock symbol:", "").upper()

    # Get stock suggestions based on user input
    stock_suggestions = get_stock_suggestions(stock_query)

    # Display stock suggestions in a selectbox
    selected_stock = st.selectbox("Select a stock:", stock_suggestions)

    # Show the selected stock
    st.write(f"You selected: {selected_stock}")

if __name__ == "__main__":
    main()






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