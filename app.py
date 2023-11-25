import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

# Initialize an empty DataFrame to store portfolio data
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = pd.DataFrame(columns=['Stock', 'Quantity', 'Purchase Date'])

# Function to add a new stock to the portfolio
def add_stock(stock_name, quantity, purchase_date):
    new_entry = pd.DataFrame({'Stock': [stock_name], 'Quantity': [quantity], 'Purchase Date': [purchase_date]})
    st.session_state['portfolio'] = pd.concat([st.session_state['portfolio'], new_entry], ignore_index=True)

# Function to plot the portfolio performance
def plot_performance():
    if not st.session_state['portfolio'].empty:
        min_date = st.session_state['portfolio']['Purchase Date'].min()
        max_date = datetime.now().strftime('%Y-%m-%d')
        portfolio_performance = pd.DataFrame()

        for index, row in st.session_state['portfolio'].iterrows():
            stock = yf.Ticker(row['Stock'])
            hist_data = stock.history(start=min_date, end=max_date)
            hist_data['Return'] = hist_data['Close'] * row['Quantity']

            # Preparing the DataFrame for addition
            if portfolio_performance.empty:
                portfolio_performance = hist_data[['Return']]
            else:
                portfolio_performance = portfolio_performance.join(hist_data[['Return']], how='outer', rsuffix='_other')
                portfolio_performance['Return'] = portfolio_performance['Return'].fillna(0) + portfolio_performance['Return_other'].fillna(0)
                portfolio_performance.drop(columns=['Return_other'], inplace=True)

        # Plotting
        if not portfolio_performance.empty:
            fig, ax = plt.subplots()
            portfolio_performance['Return'].plot(ax=ax)
            ax.set_title('Portfolio Performance Over Time')
            ax.set_ylabel('Value')
            st.pyplot(fig)


# Streamlit application layout
st.title('Portfolio Tracker')

with st.form("add_stock_form"):
    stock_name = st.text_input("Stock Symbol")
    quantity = st.number_input("Quantity", min_value=0.0, format='%f')
    purchase_date = st.date_input("Purchase Date", value=datetime.now())
    submitted = st.form_submit_button("Add to Portfolio")
    if submitted:
        add_stock(stock_name, quantity, purchase_date)

st.write("Your Portfolio:")
st.dataframe(st.session_state['portfolio'])

plot_performance()
