import streamlit as st
import requests
import datetime

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



# 2. CONTROLS SECTION (sorting and filtering)
st.markdown("### ↕️ Sort Records")
col_sort, col_reverse = st.columns(2)
with col_sort:
    sort_field = st.selectbox("Sort by column:", options=["id", "date", "amount", "category", "description"])
with col_reverse:
    sort_order = st.checkbox("Descending order (Highest / Newest first)")
st.divider()

def reset_filters():
    st.session_state.search_triggered = False
    st.session_state.filter_choice = "Category"
    st.session_state.filter_text = ""

st.markdown("### 🔍 Filter Records")
choice = st.radio("Filter by:", ["Category", "Date", "Description"], horizontal=True, key="filter_choice")

if choice == "Category":
    search_value = st.text_input("Filter by Category", placeholder="e.g. Food", key="filter_text").strip()
elif choice == "Date":
    search_value = st.text_input("Filter by Date", placeholder="YYYY-MM-DD", key="filter_text").strip()
elif choice == "Description":
    search_value = st.text_input("Filter by Description", placeholder="e.g. Lunch", key="filter_text").strip()


if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False
btn_col1, btn_col2, btn_filler = st.columns([1, 1, 4]) 
with btn_col1:
    if st.button("Search", use_container_width=True):
        st.session_state.search_triggered = True
with btn_col2:
    st.button("Reset", on_click=reset_filters, use_container_width=True)
st.divider()


# 3. DYNAMIC DATA VIEW (with deleting)
try:
    if st.session_state.search_triggered:
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
            st.divider()

            st.markdown("### 🗑️ Delete an Expense")
            delete_options = {
                f"ID: {exp['id']}  |  ₸{exp['amount']:.2f}  -  {exp['description']}": exp['id']
                for exp in expenses_to_show
            }
            
            del_col_select, del_col_btn = st.columns([2, 1])
            with del_col_select:
                selected_display = st.selectbox("Select expense to remove:", options=list(delete_options.keys()), label_visibility="collapsed")
            with del_col_btn:
                delete_button = st.button("Remove Selected Expense", type="primary", use_container_width=True)

            if delete_button:
                target_id = delete_options[selected_display]
                try:
                    del_response = requests.delete(f"{API_BASE_URL}/expenses/{target_id}")
                    if del_response.status_code == 200:
                        st.success("Expense deleted successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to delete. Code: {del_response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Server unreachable.")
        else:
            st.info("No records found matching current criteria.")
        st.divider()
    else:
        st.error(f"API Error: Received status code {response.status_code}")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Please ensure the FastAPI server is running.")



# 4. DATA ENTRY FORM
st.markdown("### ➕ Add an Expense")
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



# 5. BUDGET SECTION
st.divider()
st.markdown("### 💰 Set a Budget")
with st.form("form2"):
    month = st.text_input("Month", placeholder="YYYY-MM").strip()
    amount = st.number_input("Amount", min_value=0.01, step=1000.0, value=10000.0)
    submitted = st.form_submit_button("Set budget")

if submitted:
    if not month:
        st.error("Month field cannot be empty!")
    else:
        try:
            datetime.datetime.strptime(month, "%Y-%m")
            try:
                response = requests.put(f"{API_BASE_URL}/budget/{month}", json=amount)
                if response.status_code == 200:
                    st.success("Budget set successfully!")
                    st.rerun()
                else:
                    st.error(f"API Error: Received status code {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Could not reach backend server. Please ensure the FastAPI server is running.")
        
        except ValueError:
            st.error("Invalid format! Please use YYYY-MM")

try:
    metrics_response = requests.get(f"{API_BASE_URL}/budget/status")
    
    if metrics_response.status_code == 200:
        all_expenses = metrics_response.json()
        percentage = (all_expenses["percentage_used"]/100)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.caption("")
            st.caption("")
            st.metric(label="Monthly budget", value=f"₸{all_expenses["monthly_budget"]:.2f}")
        with col2:
            st.caption("")
            st.caption("")
            st.metric(label="Remaining", value=f"₸{all_expenses["remaining"]:.2f}")
        with col3:
            st.caption("")
            st.caption("")
            st.progress(min(percentage, 1.0), text="Percentage used")
        with col4:
            st.caption("")
            st.caption("")
            st.metric(label="Excess", value=f"₸{all_expenses["excess"]:.2f}")
        st.divider()
    else:
        st.error(f"Metrics Error: Received status code {metrics_response.status_code}")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Metrics unavailable.")