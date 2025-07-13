import streamlit as st
from ui.home import homepage
from ui.online_transactions import Online_transactions
from ui.account_details import Account_details
from ui.retrieve_data import retrieve_data
from ui.logout import logout

def after_log_reg():
    user_name = st.session_state.get("user_name", "User") ## is ky andar user ka naam araha hai or wo naam bankend/add_user.py or bankend/check_user.py sy araha hai 
    st.sidebar.title(f"Welcome, {user_name}!")

    all_option = st.sidebar.radio("Select an option", ["Home", "Online Transactions", "Account Details", "Retrieve Data", "Logout"])

    if all_option == "Home":
        homepage()
    elif all_option == "Online Transactions":
        Online_transactions()
    elif all_option == "Account Details":
        Account_details()
    elif all_option == "Retrieve Data":
        retrieve_data()
    elif all_option == "Logout":
        logout()



