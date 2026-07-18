import streamlit as st
import requests

st.subheader("Expense Tracker Dashboard")
API_BASE_URL = "http://127.0.0.1:8000"

try:
    response = requests.get(f"{API_BASE_URL}/expenses")
    
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


with st.form("form"):
    amount = st.number_input("Amount", min_value=0.01, step=10.0, value=100.0)
    category = st.text_input("Category").strip().title()
    description = st.text_input("Description").strip().capitalize()
    date = st.date_input("Date").strftime("%Y-%m-%d")
    submitted = st.form_submit_button("Add expense")

if submitted:
    if not category:
        st.error("Category fields cannot be empty!")
    elif not description:
        st.error("Description fields cannot be empty!")
    else:
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        }
        try:
            response = requests.post(f"{API_BASE_URL}/expenses", json=expense)
            if response.status_code == 201:
                st.write(f"Expense added successfully!")
                st.rerun()
            else:
                st.error(f"API Error: Received status code {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Could not reach backend server. Please ensure the FastAPI server is running.")