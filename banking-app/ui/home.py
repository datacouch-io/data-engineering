import streamlit as st
import pandas as pd
import json
from backend.find_user_data import find_user_data, read_curent_user_data

def homepage():
   
    # Custom CSS for styling
    st.markdown("""
    <style>
        .main {
            background-color: #f0f2f5;
            padding: 20px;
        }
        .sidebar .sidebar-content {
            background-color: #1e3a8a;
            color: white;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #1e40af;
        }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
    </style>
    """, unsafe_allow_html=True)

    find_user_data() ## is ko is liye dia hai q ky ye user ko filter kar raha hai password ky zayeye
    user_data = read_curent_user_data() ## ye backend/current_user_data.py sy user ka data araha hai
    
    # Filter only debit transactions
    debit_transactions = [tx for tx in user_data["account"]["transactions"] if tx["type"] == "debit"]

        
    # Sample data for transactions
    transactions_data = {
        "Date": ["2025-05-01", "2025-04-30", "2025-04-29"],
        "Description": ["Grocery Store", "Salary Credit", "Utility Bill"],
        "Amount": [-1500, 50000, -2000],
        "Balance": [48500, 50000, 2500]
    }
    df_transactions = pd.DataFrame(transactions_data)

    # Sidebar for navigation
    st.sidebar.title("Banking App")

    # Main content
    st.title("🏦 SUK Bank App")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Account Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Balance")
        st.metric("Current Account", f"Rs: {user_data['account']['balance']}", ".")
    with col2:
        st.subheader("Recent Activity")
        if debit_transactions:
            st.write(f"Last Transfer: Rs: {debit_transactions[-1]['amount']}")
        else:
            st.write(f"Last Transfer: Rs 00")
    with col3:
        st.subheader("Quick Actions")
        if st.button("Show Account Number"):
            st.write(user_data["account"]["account_number"]) 
    st.markdown('</div>', unsafe_allow_html=True)




    # Convert to DataFrame
    transactions = user_data["account"]["transactions"][0:5]
    if transactions:
        df_transactions = pd.DataFrame(transactions)

        # Format date and time
        df_transactions["Date"] = pd.to_datetime(df_transactions["transfer_date"]).dt.date
        df_transactions["Time"] = df_transactions["transfer_time"]
        df_transactions["Amount"] = df_transactions["amount"].apply(lambda x: f"₹{x:,.2f}")
        df_transactions["Type"] = df_transactions["type"].str.capitalize()
        df_transactions["To Account"] = df_transactions["to_account"]
        df_transactions["Description"] = df_transactions["description"]

        # Final columns order
        df_transactions = df_transactions[["Date", "Time", "Type", "Amount", "Description", "To Account"]]

        # Show in Streamlit
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Recent Transactions")
        st.dataframe(df_transactions)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.header("Recent Transactions")
        st.warning("🚫 No transactions found for this account.")
        st.info("Ask the user to perform some transactions to see activity here.")
        st.image("https://cdn-icons-png.flaticon.com/512/6598/6598519.png", width=200)

        