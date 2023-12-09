import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from supabase import create_client, Client

# Initialize Supabase client
SUPABASE_URL = "https://vzoizgrsdwulmwwopjvq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6b2l6Z3JzZHd1bG13d29wanZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDIxMjAwMDAsImV4cCI6MjAxNzY5NjAwMH0.vxL92OsvTj70xV-l-2eyEJl6tf3InETpqB2dVCvL-TQ" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Registration Function
def supabase_register(email, password):
    user = supabase.auth.sign_up(email=email, password=password)
    if user.get('user'):
        return True, "Registration successful. Please check your email to verify your account."
    else:
        error_message = user.get('error', {}).get('message', 'Registration failed.')
        return False, error_message

# Login Function
def supabase_login(username, password):
    user = supabase.auth.sign_in(email=username, password=password)
    if user.get('user'):
        return True, user.get('user')
    else:
        return False, None

# Function to add a holding
def add_holding(symbol, amount_of_shares, purchase_date):
    st.session_state['holdings'].append({
        'symbol': symbol,
        'amount': amount_of_shares,
        'purchase_date': purchase_date
    })

# Function to delete a holding
def delete_holding(index):
    st.session_state['holdings'].pop(index)

# Streamlit app layout
st.title("Stock Holdings Value Tracker")

# Sidebar for Registration and Login
with st.sidebar:
    st.subheader("User Authentication")

    with st.expander("Register"):
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type='password', key="reg_password")
        if st.button("Register", key="register_button"):
            success, message = supabase_register(reg_email, reg_password)
            if success:
                st.success(message)
            else:
                st.error(message)

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type='password', key="login_password")
    if st.button("Login", key="login_button"):
        login_success, user = supabase_login(username, password)
        if login_success:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = user['email']
            st.success(f"Logged in as {user['email']}")
        else:
            st.error("Incorrect username or password")

# Initialize session state for holdings
if 'holdings' not in st.session_state:
    st.session_state['holdings'] = []

# Initialize session state for logged in status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Portfolio Tracker Tab
tab1, tab2 = st.tabs(["Portfolio Tracker", "Information Tool"])

with tab1:
    if st.session_state['logged_in']:
        with st.form("Add Holding"):
            symbol = st.text_input("Enter Stock Symbol", "AAPL")
            amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0)
            purchase_date = st.date_input("Select Purchase Date")
            submitted = st.form_submit_button("Add Holding")
            if submitted:
                add_holding(symbol, amount_of_shares, purchase_date)

        for index, holding in enumerate(st.session_state['holdings']):
            st.write(f"Holding {index + 1}: {holding['symbol']} - {holding['amount']} shares")
            if st.button(f"Delete Holding {index + 1}", key=f"delete_{index}"):
                delete_holding(index)

        if st.button("Update Portfolio"):
            total_values = pd.DataFrame()
            for holding in st.session_state['holdings']:
                stock = yf.Ticker(holding['symbol'])
                data = stock.history(start=holding['purchase_date'].strftime('%Y-%m-%d'))
                holding_value = data['Close'] * holding['amount']
                holding_value.name = holding['symbol']

                if total_values.empty:
                    total_values = holding_value.to_frame()
                else:
                    total_values = total_values.join(holding_value, how='outer')

            if not total_values.empty:
                total_values['Total Value'] = total_values.sum(axis=1)
                total_values.index = total_values.index.date
                st.line_chart(total_values['Total Value'])
                st.dataframe(total_values, width=700, height=300)
    else:
        st.warning("Please login to access the Portfolio Tracker")

with tab2:

        # Function to format camelCase names into a readable format
    def format_camel_case(name):
        formatted_name = ''.join([' ' + char if char.isupper() else char for char in name]).strip()
        return formatted_name.title()

    # Function to fetch stock data
    def fetch_stock_data(symbol):
        stock = yf.Ticker(symbol)
        return stock.info

    # Function to get the original key from formatted name
    def get_original_key(formatted_name, sample_data):
        for key in sample_data.keys():
            if format_camel_case(key) == formatted_name:
                return key
        return None

    # Initialize session state for stock symbols
    if 'num_stocks' not in st.session_state:
        st.session_state['num_stocks'] = 1  # Start with 1 stock

    # Fetch data for a sample stock to get all data points
    sample_stock = yf.Ticker('AAPL')
    sample_data = sample_stock.info

    # Extract and format all available data points
    all_data_points = [format_camel_case(point) for point in sample_data.keys()]

    # Multiselect dropdown for choosing data points
    selected_data_points = st.multiselect('Select data points for comparison', all_data_points, default=['Current Price', 'Market Cap', 'Sector', 'Dividend Rate', 'Dividend Yield', 'Payout Ratio', 'Volume', 'Currency', 'Price To Book'])

    # Function to add more stocks
    def add_stock():
        st.session_state['num_stocks'] += 1

    # Button to add more stocks
    st.button('Add another stock', on_click=add_stock)

    # Create input fields dynamically based on the number of stocks
    stock_symbols = []
    for i in range(st.session_state['num_stocks']):
        symbol = st.text_input(f'Stock Symbol {i + 1}', key=f'stock_{i}')
        if symbol:
            stock_symbols.append(symbol)

    # Fetch data for entered symbols
    stock_data = [fetch_stock_data(symbol) for symbol in stock_symbols if symbol]

    # Only proceed if at least one stock has been entered
    if stock_data:
        # Adjust the data fetching to use the original keys
        comparison_data = {'Data Point': selected_data_points}
        for symbol, data in zip(stock_symbols, stock_data):
            comparison_data[symbol] = [data.get(get_original_key(point, sample_data)) for point in selected_data_points]

        # Create the DataFrame
        comparison_df = pd.DataFrame(comparison_data)

        # Styling the DataFrame
        st.write(comparison_df.style.set_properties(**{'border-color': 'black', 'border-width': '1px', 'border-style': 'solid'}).set_table_styles([{'selector': 'th', 'props': [('font-size', '16px')]}]))

    # Function to fetch YTD stock price data and normalize it
    def fetch_normalize_stock_data(symbol):
        today = datetime.today().strftime('%Y-%m-%d')
        start_of_year = datetime.today().replace(month=1, day=1).strftime('%Y-%m-%d')
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_of_year, end=today)
        # Normalize to 100 at the starting point
        normalized_df = (df['Close'] / df['Close'].iloc[0]) * 100
        return normalized_df

    # Fetch and plot data if at least one stock has been entered
    if stock_data:
        plt.figure(figsize=(10, 6))
        for symbol in stock_symbols:
            normalized_prices = fetch_normalize_stock_data(symbol)
            plt.plot(normalized_prices, label=symbol)

        plt.title("YTD Stock Price Comparison, Normalized to 100")
        plt.xlabel("Date")
        plt.ylabel("Normalized Price")
        plt.legend()
        st.pyplot(plt)