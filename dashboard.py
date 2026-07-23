import streamlit as st
import requests
import datetime
import pandas as pd
import altair as alt

st.set_page_config(page_title="Expense Tracker Dashboard", page_icon="💰", layout="wide")

st.title("Expense Tracker Dashboard")
st.divider()
API_BASE_URL = "http://127.0.0.1:8000"


# ==========================================
# 1. METRICS SECTION
# ==========================================
st.markdown("### 📋 Overview")
try:
    metrics_response = requests.get(f"{API_BASE_URL}/budget/overview")
    
    if metrics_response.status_code == 200:
        all_expenses = metrics_response.json()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Transactions", value=all_expenses["transactions"])
            st.caption("Recorded this month.")
            st.caption("")
        with col2:
            st.metric(label="Total Spent", value=f"₸{all_expenses['spent']:.2f}")
            st.caption("Across all categories this month.")
            st.caption("")

        col3, col4 = st.columns(2)
        with col3:
            st.metric(label="Monthly Budget", value=f"₸{all_expenses['monthly_budget']:.2f}")
            st.caption(f"{all_expenses['percentage_used']:.1f}% of budget used.")
        with col4:
            st.metric(label="Remaining Budget", value=f"₸{all_expenses['remaining']:.2f}")
            st.caption("Available to spend this month.")

        percentage = (all_expenses["percentage_used"] / 100.0)
        st.progress(min(percentage, 1.0))
        st.divider()
    else:
        st.error(f"Metrics Error: Received status code {metrics_response.status_code}.")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Metrics unavailable.")



# ==========================================
# 2. CHARTS & REPORTS
# ==========================================
st.markdown("### 📊 Analytics")
left_col, right_col = st.columns([0.6, 0.4], gap="large")

with left_col:
    st.markdown("##### Expense Breakdown")
    try:
        charts_response = requests.get(f"{API_BASE_URL}/reports/categories")
        
        if charts_response.status_code == 200:
            my_dict = charts_response.json()

            if my_dict:
                df = pd.DataFrame(list(my_dict.items()), columns=["Categories", "Expenses"])
                chart = (
                    alt.Chart(df)
                    .mark_arc(innerRadius=50)
                    .encode(
                        theta=alt.Theta("Expenses:Q", title="Expenses"),
                        color=alt.Color("Categories:N", title="Category")
                    )
                    .properties(height=300)
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No categorical records found to map chart metrics.")
        else:
            st.error(f"Charts Error: Received status code {charts_response.status_code}.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server. Charts unavailable.")

with right_col:
    st.markdown("##### Summary Metrics")
    try:
        reports_response = requests.get(f"{API_BASE_URL}/reports/summary")

        if reports_response.status_code == 200:
            summary = reports_response.json()
            
            highest = f"₸{summary['highest_expense']:.2f}"
            lowest = f"₸{summary['lowest_expense']:.2f}"
            avg_expense = f"₸{summary['average_expense']:.2f}"
            
            st.metric(label="Highest Expense (All-Time)", value=highest)
            st.metric(label="Lowest Expense (All-Time)", value=lowest)
            st.metric(label="Average Expense (All-Time)", value=avg_expense)
        else:
            st.error(f"Summary Error: Received status code {reports_response.status_code}.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server. Summary data unavailable.")
st.divider()



# ==========================================
# 3. TRANSACTIONS
# ==========================================
def reset_filters():
    st.session_state.search_triggered = False
    st.session_state.filter_choice = "Category"
    st.session_state.filter_text_cat = ""
    st.session_state.filter_text_date = ""
    st.session_state.filter_text_desc = ""

left_panel, right_panel = st.columns([0.4, 0.6], gap="large")
with left_panel:
    st.markdown("### ↕️ Sort Records")
    sort_field = st.selectbox("Sort by column:", options=["id", "date", "amount", "category", "description"])
    sort_order = st.checkbox("Descending order (Highest / Newest first)")

with right_panel:
    st.markdown("### 🔍 Filter Records")
    choice = st.radio("Filter by:", ["Category", "Date", "Description"], horizontal=True, key="filter_choice")

    if choice == "Category":
        search_value = st.text_input("Filter by Category", placeholder="e.g. Food", key="filter_text_cat").strip()
    elif choice == "Date":
        search_value = st.text_input("Filter by Date", placeholder="YYYY-MM-DD", key="filter_text_date").strip()
    elif choice == "Description":
        search_value = st.text_input("Filter by Description", placeholder="e.g. Lunch", key="filter_text_desc").strip()

    if "search_triggered" not in st.session_state:
        st.session_state.search_triggered = False

    btn_col1, btn_col2, btn_filler = st.columns([1, 1, 1]) 
    with btn_col1:
        if st.button("Search", use_container_width=True):
            st.session_state.search_triggered = True
            st.rerun()
    with btn_col2:
        st.button("Reset", on_click=reset_filters, use_container_width=True)

st.markdown("")
st.markdown("")
try:
    if st.session_state.search_triggered and search_value:
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
        expenses_to_show = sorted(expenses_to_show, key=lambda x: x[sort_field], reverse=sort_order)
        
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
        st.error(f"API Error: Received status code {response.status_code}.")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Please ensure the FastAPI server is running.")



# ==========================================
# 4. DATA ENTRY FORM
# ==========================================
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
                st.error(f"API Error: Received status code {response.status_code}.")
        except requests.exceptions.ConnectionError:
            st.error("Could not reach backend server. Please ensure the FastAPI server is running.")



# ==========================================
# 5. BUDGET SECTION
# ==========================================
st.divider()
st.markdown("### 💰 Budget Management")
try:
    if metrics_response.status_code == 200:

        col1, col2 = st.columns(2)
        with col1:
            st.caption("")
            st.metric(label="Current Budget", value=f"₸{all_expenses['monthly_budget']:.2f}")
            st.caption("")
        with col2:
            st.caption("")
            st.metric(label="Exceeded By", value=f"₸{all_expenses['excess']:.2f}")
            st.caption("")
    else:
        st.error(f"Could not load budget data.")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server. Backend is offline.")

current_month = datetime.date.today().strftime("%Y-%m")
with st.form("form2"):
    month = st.text_input("Month", value=current_month).strip()
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
                    st.error(f"API Error: Received status code {response.status_code}.")

            except requests.exceptions.ConnectionError:
                st.error("Could not reach backend server. Please ensure the FastAPI server is running.")
        except ValueError:
            st.error("Invalid format! Please use YYYY-MM.")



# ==========================================
# 6. AI FINANCIAL ADVISOR PANEL
# ==========================================
st.divider()
st.markdown("### 🤖 AI Financial Advisor")
st.markdown("")
st.markdown("")
ai_left, ai_right = st.columns(2, gap="large")

with ai_left:
    st.markdown("##### 📊 Automated Health Assessment")
    st.caption("Click to get an AI-generated summary of your spending.")
    
    if st.button("Analyze my finances", use_container_width=True, type="secondary"):
        with st.spinner("Analyzing your spending..."):
            
            try:
                analysis_res = requests.get(f"{API_BASE_URL}/ai/analyze")
                if analysis_res.status_code == 200:
                    st.markdown(analysis_res.json()["analysis"])
                else:
                    st.error(f"Analysis Error: Received status code {analysis_res.status_code}.")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the server. Please ensure the FastAPI server is running.")

with ai_right:
    st.markdown("##### ✨ Ask AI")
    st.caption("Ask a specific question about your spending or budget.")
    
    user_question = st.text_input(
        "Enter your query:", 
        placeholder="How can I save 30,000 ₸ this month?", 
        key="ai_chat_input"
    ).strip()
    
    if st.button("Ask", use_container_width=True, type="primary"):
        if user_question:
            with st.spinner("Getting your answer..."):

                try:
                    chat_res = requests.post(f"{API_BASE_URL}/ai/ask", json={"user_query": user_question})
                    if chat_res.status_code == 200:
                        st.info(chat_res.json()["answer"])
                    else:
                        st.error(f"API Error: Received status code {chat_res.status_code}.")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the server. Please ensure the FastAPI server is running.")
        else:
            st.warning("Question cannot be empty.")