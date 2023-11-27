# import all needed libraries
import streamlit as st
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# API Key (secure it as needed)
api_key = 'ZLEMYDXGU0STLRL1'
ts = TimeSeries(key=api_key, output_format='pandas')

# Streamlit app layout
# Title
st.title("Stock Holdings Value Tracker")

# Use a session state to store the holdings
if 'holdings' not in st.session_state:
    st.session_state['holdings'] = []

# Function to add a holding
def add_holding():
    st.session_state['holdings'].append({
        'symbol': symbol,
        'amount': amount_of_shares,
        'purchase_date': purchase_date,
        'purchase_price': purchase_price
    })

# Function to delete a holding
def delete_holding(index):
    st.session_state['holdings'].pop(index)

# User interface to add a new holding
with st.form("Add Holding"):
    symbol = st.text_input("Enter Stock Symbol", "AAPL")
    amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0.1)
    purchase_date = st.date_input("Select Purchase Date")
    purchase_price = st.number_input("Enter Purchase Price per Share", min_value=0.1)
    submitted = st.form_submit_button("Add Holding")
    if submitted:
        add_holding()

# Display current holdings with the option to delete
for index, holding in enumerate(st.session_state['holdings']):
    st.write(f"Holding {index + 1}: {holding['symbol']} - {holding['amount']} shares")
    delete_button = st.button(f"Delete Holding {index + 1}", key=f"delete_{index}")
    if delete_button:
        delete_holding(index)

# Fetch and aggregate data when 'Update Portfolio' button is clicked
if st.button("Update Portfolio"):
    total_values = pd.DataFrame()
    for holding in st.session_state['holdings']:
        try:
            data, _ = ts.get_daily(symbol=holding['symbol'], outputsize='compact')
            data_filtered = data[data.index >= holding['purchase_date'].strftime('%Y-%m-%d')]
            holding_value = data_filtered['4. close'] * holding['amount']
            total_values[holding['symbol']] = holding_value
        except Exception as e:
            st.error(f"Error fetching data for {holding['symbol']}: {e}")

    # Display data as a line chart
    if not total_values.empty:
        total_values['Total Value'] = total_values.sum(axis=1)
        st.line_chart(total_values['Total Value'])

        # Display the data in a table format
        st.write(total_values)

# Piechart visualization
if st.button("Show Portfolio Composition"):
    current_values = {}
    total_portfolio_value = 0
    for holding in st.session_state['holdings']:
        try:
            data, _ = ts.get_daily(symbol=holding['symbol'], outputsize='compact')
            most_recent_close = data['4. close'].iloc[-1]
            current_value = most_recent_close * holding['amount']
            current_values[holding['symbol']] = current_value
            total_portfolio_value += current_value
        except Exception as e:
            st.error(f"Error fetching data for {holding['symbol']}: {e}")

    if total_portfolio_value > 0:
        labels = current_values.keys()
        sizes = current_values.values()

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Portfolio Composition')

        st.pyplot(plt)
    else:
        st.write("No holdings to display.")
