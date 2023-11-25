import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize an empty DataFrame to store portfolio data
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = pd.DataFrame(columns=['Stock', 'Quantity'])

# Function to add a new stock to the portfolio
def add_stock(stock_name, quantity):
    new_entry = pd.DataFrame({'Stock': [stock_name], 'Quantity': [quantity]})
    st.session_state['portfolio'] = pd.concat([st.session_state['portfolio'], new_entry], ignore_index=True)

# Function to plot the portfolio
def plot_portfolio():
    if not st.session_state['portfolio'].empty:
        fig, ax = plt.subplots()
        st.session_state['portfolio'].groupby('Stock')['Quantity'].sum().plot(kind='bar', ax=ax)
        ax.set_title('Portfolio Distribution')
        ax.set_ylabel('Quantity')
        st.pyplot(fig)

# Streamlit application layout
st.title('Portfolio Tracker')

with st.form("add_stock_form"):
    stock_name = st.text_input("Stock Symbol")
    quantity = st.number_input("Quantity", min_value=0.0, format='%f')
    submitted = st.form_submit_button("Add to Portfolio")
    if submitted:
        add_stock(stock_name, quantity)

st.write("Your Portfolio:")
st.dataframe(st.session_state['portfolio'])

plot_portfolio()
