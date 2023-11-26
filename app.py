import streamlit as st
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# Hardcoded API key (replace 'YOUR_API_KEY' with your actual API key)
api_key = ZLEMYDXGU0STLRL1

# Function to fetch stock data
def get_stock_data(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, _ = ts.get_quote_endpoint(symbol=symbol)
    return data

# Streamlit app layout
st.title('Stock Portfolio Tracker')

# User input for adding stocks to the portfolio
with st.form("portfolio_form"):
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)").upper()
    shares = st.number_input("Enter number of shares", min_value=0, value=0, step=1)
    submitted = st.form_submit_button("Add to Portfolio")

# Placeholder for displaying the portfolio
portfolio_container = st.empty()

# Store portfolio in a session state to persist data
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=['Symbol', 'Shares', 'Price', 'Total Value'])

# If a stock is added
if submitted and symbol and shares > 0:
    try:
        stock_data = get_stock_data(symbol, api_key)
        price = stock_data['05. price'][0]
        st.session_state.portfolio = st.session_state.portfolio.append({
            'Symbol': symbol,
            'Shares': shares,
            'Price': price,
            'Total Value': shares * float(price)
        }, ignore_index=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display the portfolio
with portfolio_container:
    if not st.session_state.portfolio.empty:
        st.write("Your Portfolio:")
        st.dataframe(st.session_state.portfolio)
        total_value = st.session_state.portfolio['Total Value'].sum()
        st.write(f"Total Portfolio Value: ${total_value:.2f}")
    else:
        st.write("Your portfolio is empty. Add some stocks to track!")

# Additional features can be added here (like removing stocks, updating prices, etc.)
