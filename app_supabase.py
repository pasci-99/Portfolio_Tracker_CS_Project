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
st.title("Hey " + st.session_state['username'])


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