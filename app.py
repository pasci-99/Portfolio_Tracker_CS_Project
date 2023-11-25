import streamlit as st
import pandas as pd

# Initialize an empty DataFrame to store portfolio data
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = pd.DataFrame(columns=['Stock', 'Quantity'])

# Function to add a new stock to the portfolio
def add_stock(stock_name, quantity):
    new_entry = {'Stock': stock_name, 'Quantity': quantity}
    st.session_state['portfolio'] = st.session_state['portfolio'].append(new_entry, ignore_index=True)

# Streamlit application layout
st.title('Portfolio Tracker')

with st.form("add_stock_form"):
    stock_name = st.text_input("Stock Symbol")
    quantity = st.number_input("Quantity", min_value=0.0, format='%f')
    submitted = st.form_submit_button("Add to Portfolio")
    if submitted:
        add_stock(stock_name, quantity)

st.write("Your Portfolio:")
st.write(st.session_state['portfolio'])
