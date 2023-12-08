import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for storing portfolio
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []

# Function to store input data as a holding dictionary and append to session state portfolio
def add_holding():
    holding = {
        'symbol': symbol,
        'shares': amount_of_shares,
        'purchase_date': str(purchase_date)
    }
    st.session_state['portfolio'].append(holding)

# Function to delete a holding from the portfolio
def delete_holding(index):
    del st.session_state['portfolio'][index]

# Form for adding holdings
with st.form("Add Holding"):
    symbol = st.text_input("Enter Stock Symbol", "AAPL")
    amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0)
    purchase_date = st.date_input("Select Purchase Date")
    submitted = st.form_submit_button("Add Holding", on_click=add_holding)

# Display current portfolio with option to delete each holding
st.write("Current Portfolio:")
for i, holding in enumerate(st.session_state['portfolio']):
    st.text(f"{holding['symbol']} - {holding['shares']} shares - Purchased on: {holding['purchase_date']}")
    if st.button("Delete", key=i):
        delete_holding(i)

