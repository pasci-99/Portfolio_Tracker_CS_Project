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


if st.button('Write'):
    st.write('Hello')


st.write(st_supabase_client.query("*", table="test").execute().data)

""" # Initialize connection HELLO WORLD.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="mytable", ttl="10m").execute()

# Print results.
for row in rows.data:
    st.write(f"{row['name']} has a :{row['pet']}:") """

st_supabase_client.table("test").insert(
    [{"test": "Eyo crazy motherfucker"}, {"test": "How you doin?"}], count="None"
).execute()