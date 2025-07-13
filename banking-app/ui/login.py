import streamlit as st
from backend.check_user import CheckUser

def login():
    fristName : str = st.text_input("Enter Your Frist Name:")
    lastName: str = st.text_input("Enter Your Last Name:")
    email : str = st.text_input("Enter Your Email:")
    password : str = st.text_input("Enter Your Password:")

    if st.button("Login"):
        if fristName == "" and lastName == "" and email == "" and password == "":
            st.warning("Please fill all fields correctly.")
        else :
            data : CheckUser = CheckUser(fristName, lastName, email, password)
            checkUser = data.check_user() # ye check karry ga ky user register hai aya nhi. hai to True aye ga wana False aye ga

            if checkUser:
                st.success("Login Successfully")
                return True
            else:
                st.warning("Invaild Your email and password")
                return False

          
