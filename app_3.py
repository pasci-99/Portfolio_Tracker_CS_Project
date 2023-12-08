import streamlit as st
import yfinance as yf
import pandas as pd

# Initialize session state for storing portfolio
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []

# Function to store input data as a holding dictionary and append to session state portfolio
def add_holding(symbol, number_of_shares, purchase_date):
    holding = {
        'symbol': symbol,
        'shares': number_of_shares,
        'purchase_date': str(purchase_date)
    }
    st.session_state['portfolio'].append(holding)

# Form for adding holdings
with st.form("Add Holding"):
    symbol = st.text_input("Enter Stock Symbol", "AAPL")
    number_of_shares = st.number_input("Enter the Number of Shares", min_value=0)
    purchase_date = st.date_input("Select Purchase Date")
    submitted = st.form_submit_button("Add Holding")

    if submitted:
        add_holding(symbol, number_of_shares, purchase_date)

# Display current portfolio with option to delete each holding
st.write("Current Portfolio:")
for i, holding in enumerate(st.session_state['portfolio']):
    st.text(f"{holding['symbol']} - {holding['shares']} shares - Purchased on: {holding['purchase_date']}")
    if st.button("Delete", key=f"delete_{i}"):
        del st.session_state['portfolio'][i]
        st.experimental_rerun()

# Function to fetch stock data
def fetch_stock_data(symbol, start_date):
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date)
    return hist['Close']

# Function to calculate portfolio value
def calculate_portfolio_value(portfolio):
    if not portfolio:
        return pd.DataFrame()  # Return empty DataFrame if portfolio is empty

    earliest_date = min([pd.to_datetime(holding['purchase_date']) for holding in portfolio])
    portfolio_values = pd.DataFrame(index=pd.date_range(start=earliest_date, end=pd.Timestamp('today')))

    for holding in portfolio:
        stock_data = fetch_stock_data(holding['symbol'], holding['purchase_date'])
        holding_value = stock_data * holding['shares']
        holding_value = holding_value.reindex(portfolio_values.index).fillna(0)
        portfolio_values[holding['symbol']] = holding_value

    portfolio_values['Total Value'] = portfolio_values.sum(axis=1)
    return portfolio_values

# Calculate and display portfolio value if the portfolio is not empty
if st.session_state['portfolio']:
    portfolio_values_df = calculate_portfolio_value(st.session_state['portfolio'])
    st.line_chart(portfolio_values_df['Total Value'])
