import streamlit as st
import pandas as pd
from backend.find_user_data import read_curent_user_data

def retrieve_data():
    user_data = read_curent_user_data()

    # Get transaction data
    transactions = user_data["account"]["transactions"]
    if transactions:
        df_transactions = pd.DataFrame(transactions)

        # Convert date column to datetime for proper filtering
        df_transactions["transfer_date"] = pd.to_datetime(df_transactions["transfer_date"])

        st.header("📊 Retrieve Transaction Data")

        option = st.selectbox("Select filter:", [
            "All Transactions",
            "By Date",
            "By Type (Credit/Debit)",
            "By Description"
        ])

        # Filters
        date = None
        txn_type = None
        desc = ""

        if option == "By Date":
            date = st.date_input("Select Date")
        elif option == "By Type (Credit/Debit)":
            txn_type = st.selectbox("Select Type", ["credit", "debit"])
        elif option == "By Description":
            desc = st.text_input("Enter Description")

        if st.button("Show Results"):
            if option == "All Transactions":
                st.dataframe(df_transactions)

            elif option == "By Date":
                filtered = df_transactions[
                    df_transactions["transfer_date"].dt.date == date
                ]
                st.dataframe(filtered)

            elif option == "By Type (Credit/Debit)":
                filtered = df_transactions[
                    df_transactions["type"].str.lower() == txn_type.lower()
                ]
                st.dataframe(filtered)

            elif option == "By Description":
                filtered = df_transactions[
                    df_transactions["description"].str.contains(desc, case=False, na=False)
                ]
                st.dataframe(filtered)
    else:
        st.warning("🚫 No transactions found for this account.")
        st.info("Ask the user to perform some transactions to see activity here.")
        st.image("https://cdn-icons-png.flaticon.com/512/6598/6598519.png", width=200)
