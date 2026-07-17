import streamlit as st
import requests

st.subheader("Expense Tracker Dashboard")

try:
    response = requests.get("http://127.0.0.1:8000/expenses")
    
    if response.status_code == 200:
        expenses = response.json()
        if expenses:
            st.dataframe(expenses, use_container_width=True)
        else:
            st.info("The database is currently empty.")
    else:
        st.error(f"API Error: Received status code {response.status_code}")

except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Please ensure the FastAPI server is running.")

