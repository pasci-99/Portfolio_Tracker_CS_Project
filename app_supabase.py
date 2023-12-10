# streamlit_app.py

import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import date

st_supabase_client = st.connection(
    name="pasci99connection",
    type=SupabaseConnection,
    ttl=None,
    url="https://pulfkaxpvhgvgvlgjpaj.supabase.co",
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1bGZrYXhwdmhndmd2bGdqcGFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDIxNTkzNzIsImV4cCI6MjAxNzczNTM3Mn0.twkOSqpf4M7qVREItNHb19rG7iWNli-dtc2DSdEdBlQ",
)

# Initialize the session state variable if not present
if 'username' not in st.session_state:
    st.session_state['username'] = ""
st.title("Oi " + st.session_state['username'])


with st.form("Login"):
        myUserName = st.text_input("Enter your username")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.session_state['username'] = myUserName

if st.session_state['username'] != "":
    if st.button("Read"):
        response = st_supabase_client.query("*", table="test", ttl=0).execute()
        st.write("Filtered by username:")
        st.write([obj for obj in response.data if obj.get('username') == myUserName])

    if st.button('Write'):
        st.write(st_supabase_client.table("test").insert(
        [{"test": "APPL", "username": st.session_state['username']}], count="None"



).execute())
        

def delete_holding(holding_id):
    # Execute the delete query
    response = st_supabase_client.table("portfolio").delete().eq('id', holding_id).execute()
    # After deletion, you may want to refresh the data displayed

def display_holdings():
    myUserName = st.session_state.get('username')
    response = st_supabase_client.query("*", table="portfolio", ttl=0).execute()
    filtered_data = [obj for obj in response.data if obj.get('username') == myUserName]


if st.session_state['username'] != "":
    with st.form("Add Holding"):
        # Input fields to collect the data from the user
        symbol = st.text_input("Enter Stock Symbol")
        amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0.01, step=0.01, format="%.2f")
        purchase_date = st.date_input("Select Purchase Date")
        
        # Form submission button
        submitted = st.form_submit_button("Add Holding")


    if submitted and st.session_state.get('username'):
        # Convert the date to a string in ISO format before sending it to Supabase
        formatted_purchase_date = purchase_date.isoformat() if isinstance(purchase_date, date) else purchase_date
        
        response = st_supabase_client.table("portfolio").insert(
            [{
                "stock_symbol": symbol, 
                "quantity": amount_of_shares, 
                "purchase_date": formatted_purchase_date,
                "username": st.session_state['username']  # or username if you have it
            }]
        ).execute()

    if st.button("Display Holdings"):
        # Get the current user's username
        myUserName = st.session_state.get('username')

        # Execute the query to fetch all data from the 'portfolio' table
        response = st_supabase_client.query("*", table="portfolio", ttl=0).execute()

        # Filter the records in Python
        filtered_data = [obj for obj in response.data if obj.get('username') == myUserName]
        
        # Display the filtered data
        st.write("Holdings for username:", myUserName)
        
        for holding in filtered_data:
            col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
            with col1:
                st.write(holding['stock_symbol'])
            with col2:
                st.write(holding['quantity'])
            with col3:
                st.write(holding['purchase_date'])
            with col4:
                # Use the holding's ID to create a unique key for the button
                delete_button = st.button("Delete Holding", key=f"delete_{holding['id']}")
                if delete_button:
                    # Use the holding's ID to delete the correct holding
                    response = st_supabase_client.table("portfolio").delete().eq('id', holding['id']).execute()