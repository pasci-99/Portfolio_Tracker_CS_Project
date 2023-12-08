import streamlit as st
import yfinance as yf
import pandas as pd

# Streamlit app layout
st.title("Stock Holdings Value Tracker")

# User definition
users = {
    "Magdalena": "Test1",
    "Peter": "Test2"
    # More users possible here
}

# Login UI
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type='password')

# Function to verify credentials
def check_credentials(username, password):
    return username in users and users[username] == password

# Verify users
if st.sidebar.button("Login"):
    if check_credentials(username, password):
        st.success("Logged in as {}".format(username))
    else:
        st.error("Incorrect username or password")

# Initialize holdings
if 'holdings' not in st.session_state:
    st.session_state['holdings'] = []

# Function to add a holding
def add_holding():
    st.session_state['holdings'].append({
        'symbol': symbol,
        'amount': amount_of_shares,
        'purchase_date': purchase_date
    })

# Function to delete a holding
def delete_holding(index):
    st.session_state['holdings'].pop(index)

# User interface to add a new holding
with st.form("Add Holding"):
    symbol = st.text_input("Enter Stock Symbol", "AAPL")
    amount_of_shares = st.number_input("Enter the Number of Shares")
    purchase_date = st.date_input("Select Purchase Date")
    submitted = st.form_submit_button("Add Holding")
    if submitted:
        add_holding()

# Display current holdings
for index, holding in enumerate(st.session_state['holdings']):
    st.write(f"Holding {index + 1}: {holding['symbol']} - {holding['amount']} shares")
    if st.button(f"Delete Holding {index + 1}", key=f"delete_{index}"):
        delete_holding(index)

# Fetch data and calculate portfolio value
if st.button("Update Portfolio"):
    total_values = None
    for holding in st.session_state['holdings']:
        stock = yf.Ticker(holding['symbol'])
        data = stock.history(start=holding['purchase_date'].strftime('%Y-%m-%d'))
        data['Holdings Value'] = data['Close'] * holding['amount']
        if total_values is None:
            total_values = data[['Holdings Value']]
        else:
            total_values = total_values.join(data[['Holdings Value']], how='outer', rsuffix='_other')
            total_values['Holdings Value'] = total_values.sum(axis=1)

    # Display data as a line chart
    if total_values is not None:
        st.line_chart(total_values['Holdings Value'])

        # Display the data in a table format
        st.write(total_values)
