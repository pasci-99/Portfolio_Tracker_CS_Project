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

st.title("Oiii mate")

with st.form("Login"):
        myUserName = st.text_input("Enter your username")
        submitted = st.form_submit_button("Login")
        if submitted:
            response = st_supabase_client.select("*", table="test").execute()
        
            if response.status_code == 200:
                st.write(response.data)
                st.write("Filtered by username:")
                st.write(filter_by_username(response.data))
            else:
                st.error(f"Error: {response.text}")

def filter_by_username(data):
    # Assuming data is a list of dictionaries with the specified properties
    filtered_objects = [obj for obj in data if obj.get('username') == 'jonas']
    return filtered_objects


""" if st.button('Write'):
    st.write(st_supabase_client.table("test").insert(
    [{"test": "Eyo crazy motherfucker"}, {"test": "How you doin?"}], count="None"
).execute()) """




""" # Initialize connection HELLO WORLD.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="mytable", ttl="10m").execute()

# Print results.
for row in rows.data:
    st.write(f"{row['name']} has a :{row['pet']}:") """