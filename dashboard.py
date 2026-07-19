import streamlit as st
import requests

st.title("Expense Tracker Dashboard")
st.divider()
API_BASE_URL = "http://127.0.0.1:8000"


# 1. METRICS SECTION
try:
    metrics_response = requests.get(f"{API_BASE_URL}/expenses")
    
    if metrics_response.status_code == 200:
        all_expenses = metrics_response.json()
        total_spent = sum(item["amount"] for item in all_expenses)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total Expenses", value=len(all_expenses))
            st.caption("Transactions recorded")
        with col2:
            st.metric(label="Total Spent", value=f"₸{total_spent:.2f}")
            st.caption("Across all categories")
        st.divider()
    else:
        st.error(f"Metrics Error: Received status code {metrics_response.status_code}")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Metrics unavailable.")



# 2. CONTROLS SECTION
st.markdown("### ↕️ Sort Records")
col_sort, col_reverse = st.columns(2)

with col_sort:
    sort_field = st.selectbox("Sort by column:", options=["id", "date", "amount", "category", "description"])
with col_reverse:
    sort_order = st.checkbox("Descending order (Highest / Newest first)")
st.divider()

st.markdown("### 🔍 Filter Records")
choice = st.radio("Filter by:", ["Category", "Date", "Description"], horizontal=True)

if choice == "Category":
    search_value = st.text_input("Filter by Category", placeholder="e.g. Food").strip()
elif choice == "Date":
    search_value = st.text_input("Filter by Date", placeholder="YYYY-MM-DD").strip()
elif choice == "Description":
    search_value = st.text_input("Filter by Description", placeholder="e.g. Lunch").strip()

search_triggered = st.button("Search")
st.divider()



# 3. DYNAMIC DATA VIEW
try:
    if search_triggered and search_value:
        if choice == "Category":
            FETCH_URL = f"{API_BASE_URL}/filtered/category"
            query_params = {"category": search_value}
        elif choice == "Date":
            FETCH_URL = f"{API_BASE_URL}/filtered/date"
            query_params = {"date": search_value}
        elif choice == "Description":
            FETCH_URL = f"{API_BASE_URL}/filtered/description"
            query_params = {"description": search_value}
    else:
        FETCH_URL = f"{API_BASE_URL}/expenses/sorted"
        query_params = {"field": sort_field, "reverse": sort_order}

    response = requests.get(FETCH_URL, params=query_params)
    
    if response.status_code == 200:
        expenses_to_show = response.json()

        if expenses_to_show:
            st.dataframe(expenses_to_show, use_container_width=True)
        else:
            st.info("No records found matching current criteria.")
        st.divider()
    else:
        st.error(f"API Error: Received status code {response.status_code}")

except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Please ensure the FastAPI server is running.")



# 4. DATA ENTRY FORM
st.markdown("### ➕ Add Expense")
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
                st.success("Expense added successfully!")
                st.rerun()
            else:
                st.error(f"API Error: Received status code {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Could not reach backend server. Please ensure the FastAPI server is running.")