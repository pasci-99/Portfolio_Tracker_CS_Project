# streamlit_app.py

import streamlit as st
from st_supabase_connection import SupabaseConnection

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
st.title("Oiii " + st.session_state['username'])


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
        

with st.form("Add Holding"):
    # Input fields to collect the data from the user
    symbol = st.text_input("Enter Stock Symbol")
    amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0.01, step=0.01, format="%.2f")
    purchase_date = st.date_input("Select Purchase Date")
    
    # Form submission button
    submitted = st.form_submit_button("Add Holding")
    
    if submitted and st.session_state.get('username'):
        # Use the username from the session state as the user_id
        user_id = st.session_state['username']  # This is the username being used as a user_id
        
        # Perform the insert operation to the Supabase table
        response = st_supabase_client.table("portfolio").insert(
            [{
                "stock_symbol": symbol, 
                "quantity": amount_of_shares, 
                "purchase_date": purchase_date,
                "user_id": user_id  # Insert the username as the user_id
            }]
        ).execute()
        
        # Check if the insert operation was successful
        if response.status_code == 201:
            st.success("Portfolio entry added successfully!")
        else:
            st.error("Failed to add portfolio entry. Please try again.")

