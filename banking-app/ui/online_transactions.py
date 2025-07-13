import streamlit as st
from backend.transfer_money import TransferMoney

def Online_transactions():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Transfer Money")
    with st.form("transfer_form"):
        account_number = st.text_input("Account Number")
        amount = st.number_input("Amount (Rs)", min_value=20, step=100)
        description = st.text_area("Description")
        submitted = st.form_submit_button("Transfer")

        if submitted:
            if account_number and amount and description:
                transfer_money : TransferMoney = TransferMoney(int(account_number), int(amount), description) ##  ye ek object hai is ky zaye ye transfer hoye ga
                current_user_data = transfer_money.current_account() ##ye object ka method hai or is ky andar jo current hai us ky data ko handle kar raha hai
                if current_user_data == True:
                    transfer_user_data = transfer_money.transfer_account() ## is ky zayeye transfer hoye ga
                    st.success(f"Successfull Transfer of Rs: {amount} to  {account_number}  initiated!")
                elif current_user_data == "You don't have balance in your account.":
                    st.warning("You don't have balance in your account.")
                elif current_user_data == "This account was not found":
                    st.warning("This account was not found")
                else:
                    st.warning("Something Was Wrong")
            else:
                st.warning("Please Fill All Field")
    st.markdown('</div>', unsafe_allow_html=True)