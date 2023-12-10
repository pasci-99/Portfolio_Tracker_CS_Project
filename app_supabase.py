# streamlit_app.py

import streamlit as st
from supabase import create_client, Client
from datetime import date

supabase: Client = create_client("https://pulfkaxpvhgvgvlgjpaj.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1bGZrYXhwdmhndmd2bGdqcGFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDIxNTkzNzIsImV4cCI6MjAxNzczNTM3Mn0.twkOSqpf4M7qVREItNHb19rG7iWNli-dtc2DSdEdBlQ")

# Initialize the session state variable if not present
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# Get the current user's username
myUserName = st.session_state.get('username')
st.title("Oii " + myUserName)

if myUserName == "":
    # region USER IS NOT LOGGED IN
    with st.form("Login"):
        enteredUsername = st.text_input("Enter your username")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.session_state['username'] = enteredUsername
    # endregion
else:
    # region USER IS LOGGED IN
    # region Add Holding Form
    with st.form("Add Holding"):
        # Input fields to collect the data from the user
        symbol = st.text_input("Enter Stock Symbol")
        amount_of_shares = st.number_input("Enter the Number of Shares", min_value=0.01, step=0.01, format="%.2f")
        purchase_date = st.date_input("Select Purchase Date")
        
        # Form submission button
        submitted = st.form_submit_button("Add Holding")

    if submitted:
        # Convert the date to a string in ISO format before sending it to Supabase
        formatted_purchase_date = purchase_date.isoformat() if isinstance(purchase_date, date) else purchase_date
        
        response = supabase.table("portfolio").insert(
            {
                "stock_symbol": symbol, 
                "quantity": amount_of_shares, 
                "purchase_date": formatted_purchase_date,
                "username": myUserName
            }
        ).execute()
        st.write("Holding added!")
    # endregion

    # region Holdings Table
    # Execute the query to fetch all data from the 'portfolio' table
    response = supabase.table("portfolio").select("*").eq("username", myUserName).execute()

    # Display the filtered data

    st.header("Your holdings (Header):")

    st.write("Your holdings:")
        

    for holding in response.data:
        col1, col2, col3, col4 = st.columns([3, 3, 3, 3])
        with col1:
            st.write(holding['stock_symbol'])
        with col2:
            st.write(holding['quantity'])
        with col3:
            st.write(holding['purchase_date'])
        with col4:
            # Use a unique key for each button
            if st.button("Delete", key=f"delete_{holding['id']}"):
                response = supabase.table("portfolio").delete().eq('id', holding['id']).execute()
                st.rerun()
    # endregion
    # endregion