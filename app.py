# import all needed libraries
import streamlit as st
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

# API Key (maybe make it more secure, not sure yet how to do it)
api_key = 'ZLEMYDXGU0STLRL1'
ts = TimeSeries(key=api_key, output_format='pandas')

# Streamlit app layout
#Title
st.title("Stock Holdings Value Tracker")


# Use a session state to store the holdings. This is needed, that the user doesn't lose the inserted information when rerunning the app (clicking a button).
# Using an if clause because only needed if holdings is not existing already
if 'holdings' not in st.session_state:
    st.session_state['holdings'] = []

# Function to add a holding (Ticker, Amount, Date, Price)
def add_holding():
    st.session_state['holdings'].append({
        'symbol': symbol,
        'amount': amount_of_shares,
        'purchase_date': purchase_date,
        'purchase_price': purchase_price
    })

# Function to delete an adde holding from the holdings using the pop function
def delete_holding(index):
    st.session_state['holdings'].pop(index)

# User interface to add a new holding
with st.form("Add Holding"):
    symbol = st.text_input("Enter Stock Symbol", "AAPL")
    amount_of_shares = st.number_input("Enter the Number of Shares")
    purchase_date = st.date_input("Select Purchase Date")
    purchase_price = st.number_input("Enter Purchase Price per Share")
    submitted = st.form_submit_button("Add Holding")
    if submitted:
        add_holding()

# Display current holdings with the option to delete holdings
for index, holding in enumerate(st.session_state['holdings']):
    st.write(f"Holding {index + 1}: {holding['symbol']} - {holding['amount']} shares")
    if st.button(f"Delete Holding {index + 1}"):
        delete_holding(index)

# Fetch and aggregate data when 'Fetch Data' button is clicked
if st.button("Update Portfolio"):
    total_values = None
    for holding in st.session_state['holdings']:
        # meta_data probably not needed, can still be deleted and outputsize can maybe be adjusted to 'compact' if full length is not needed for a certain holding.
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
