import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for storing portfolio
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []

# Function to store input data as a holding dictionary and append to session state portfolio
def add_holding(symbol, amount_of_shares, purchase_date):
    holding = {
        'symbol': symbol,
        'shares': amount_of_shares,
        'purchase_date': str(purchase_date)
    }
    st.session_state['portfolio'].append(holding)

# Function to fetch stock data
def fetch_stock_data(symbol, start_date):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date)
        return hist['Close']
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.Series()

# Function to calculate portfolio value
def calculate_portfolio_value(portfolio):
    portfolio_df = pd.DataFrame()
    earliest_date = min(holding['purchase_date'] for holding in portfolio)

    for holding in portfolio:
        stock_data = fetch_stock_data(holding['symbol'], earliest_date)
        holding_value = stock_data * holding['shares']
        holding_value = holding_value.reindex(portfolio_df.index.union(stock_data.index)).fillna(0)
        
        if portfolio_df.empty:
            portfolio_df = holding_value.to_frame(holding['symbol'])
        else:
            portfolio_df = portfolio_df.join(holding_value.to_frame(holding['symbol']), how='outer')

    portfolio_df.fillna(0, inplace=True)
    return portfolio_df.sum(axis=1)

# Form for adding holdings
with st.form("Add Holding"):
    symbol_input = st.text_input("Enter Stock Symbol", "AAPL")
    shares_input = st.number_input("Enter the Number of Shares", min_value=0)
    date_input = st.date_input("Select Purchase Date")
    submitted = st.form_submit_button("Add Holding")

    if submitted:
        add_holding(symbol_input, shares_input, date_input)
        st.experimental_rerun() # Rerun to refresh the data and display updated portfolio

# Display current portfolio with option to delete each holding
st.write("Current Portfolio:")
for i, holding in enumerate(st.session_state['portfolio']):
    st.text(f"{holding['symbol']} - {holding['shares']} shares - Purchased on: {holding['purchase_date']}")
    if st.button("Delete", key=f"delete_{i}"):
        del st.session_state['portfolio'][i]
        st.experimental_rerun() # refreshes the page and updates the portfolio.

# Calculate and display portfolio value if the portfolio is not empty
if st.session_state['portfolio']:
    portfolio_value = calculate_portfolio_value(st.session_state['portfolio'])
    st.line_chart(portfolio_value)
