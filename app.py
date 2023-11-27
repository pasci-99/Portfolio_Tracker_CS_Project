import streamlit as st
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

# API Key
api_key = 'ZLEMYDXGU0STLRL1'
ts = TimeSeries(key=api_key, output_format='pandas')

# Streamlit app layout
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

# User input to add a new holding
with st.form("Add Holding"):
    symbol = st.text_input("Enter Stock Symbol", "AAPL")
    amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0.1)
    purchase_date = st.date_input("Select Purchase Date")
    purchase_price = st.number_input("Enter Purchase Price per Share", min_value=0.1)
    submitted = st.form_submit_button("Add Holding")
    if submitted:
        add_holding()

# Display current holdings and option to delete
for index, holding in enumerate(st.session_state['holdings']):
    st.write(f"Holding {index + 1}: {holding['symbol']} - {holding['amount']} shares")
    if st.button(f"Delete Holding {index + 1}"):
        delete_holding(index)

# Fetch and aggregate data when 'Fetch Data' button is clicked
if st.button("Fetch Data"):
    total_values = None
    for holding in st.session_state['holdings']:
        data, meta_data = ts.get_daily(symbol=holding['symbol'], outputsize='full')
        data_filtered = data[data.index >= holding['purchase_date'].strftime('%Y-%m-%d')]
        data_filtered['Holdings Value'] = data_filtered['4. close'] * holding['amount']
        if total_values is None:
            total_values = data_filtered[['Holdings Value']]
        else:
            total_values = total_values.join(data_filtered[['Holdings Value']], how='outer', rsuffix='_other')
            total_values['Holdings Value'] = total_values.sum(axis=1)

    # Display data as a line chart
    if total_values is not None:
        st.line_chart(total_values['Holdings Value'])

        # Display the data in a table format
        st.write(total_values)
