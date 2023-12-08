import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for storing portfolio
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []

# Function which stores the inputed data (from interface) as a holding dictionary and appends the information to the session state portfolio. If a user enters a stock twice, with different amount and purchas date, it gets trreated as a seperate holding.
def add_holding():
    holding = {
        'symbol': symbol,
        'shares': amount_of_shares,
        'purchase_date': str(purchase_date)
    }
    st.session_state['portfolio'].append(holding)

    # Form for adding holdings
with st.form("Add Holding"):
    symbol = st.text_input("Enter Stock Symbol", "AAPL")
    amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0)
    purchase_date = st.date_input("Select Purchase Date")
    submitted = st.form_submit_button("Add Holding", on_click=add_holding)


# Function to fetch data and calculate portfolio value
def calculate_portfolio_value():
    # Initialize a DataFrame to store combined portfolio data
    portfolio_df = pd.DataFrame()

    for holding in st.session_state['portfolio']:
        stock = yf.Ticker(holding['symbol'])
        hist = stock.history(start=holding['purchase_date'])
        hist['Value'] = hist['Close'] * holding['shares']
        portfolio_df = portfolio_df.add(hist['Value'], fill_value=0)
    
    return portfolio_df

# Display current portfolio
if 'portfolio' in st.session_state:
    st.write("Current Portfolio:")
    st.table(st.session_state['portfolio'])

    # Recalculate and display portfolio value if there are holdings
    if st.session_state['portfolio']:
        portfolio_value = calculate_portfolio_value()
        st.line_chart(portfolio_value)

