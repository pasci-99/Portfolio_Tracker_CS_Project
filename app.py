import streamlit as st
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime

# API Key, maybe it has to be adjusted to be more secure
api_key = ZLEMYDXGU0STLRL1
ts = TimeSeries(key=api_key, output_format='pandas')

# Streamlit app layout
st.title("Stock Holdings Value Tracker")

# User inputs
symbol = st.text_input("Enter Stock Symbol", "AAPL")
amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0.1, step=0.1, format='%f')
purchase_date = st.date_input("Select Purchase Date")
purchase_price = st.number_input("Enter Purchase Price per Share", min_value=0.1, step=0.1, format='%f')

# Fetching data when 'Fetch Data' button is clicked
if st.button("Fetch Data"):
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')

    # Filter data based on the purchase date
    data_filtered = data[data.index >= purchase_date.strftime('%Y-%m-%d')]

    # Calculate holdings value
    data_filtered['Holdings Value'] = data_filtered['4. close'] * amount_of_shares

    # Display data as a line chart
    st.line_chart(data_filtered['Holdings Value'])

    # Display the data in a table format
    st.write(data_filtered)
