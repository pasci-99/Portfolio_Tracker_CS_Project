import streamlit as st
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime

# API Key, maybe it has to be adjusted to be more secure
api_key = ZLEMYDXGU0STLRL1
ts = TimeSeries(key=api_key, output_format='pandas')

# Streamlit app layout
st.title("Stock Data Fetcher")

# User inputs
symbol = st.text_input("Enter Stock Symbol", "AAPL")
start_date = st.date_input("Select Start Date")
start_time = st.time_input("Select Start Time")
amount = st.number_input("Enter the Amount of Stocks Purchased")

# Combining date and time into a single datetime object
start_datetime = datetime.combine(start_date, start_time)

# Fetching data when 'Fetch Data' button is clicked
if st.button("Fetch Data"):
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    
    # Filter data based on the start_datetime
    data_filtered = data[data.index >= start_datetime]
    
    # Display data
    st.write(data_filtered)
