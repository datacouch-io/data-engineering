import streamlit as st
from backend.add_user import AddUser
import time

def rigister():
    fristName : str = st.text_input("Enter Your Frist Name")
    lastName: str = st.text_input("Enter Your Last Name")
    age : int = st.text_input("Enter Your Age")
    email : str = st.text_input("Enter Your Email")
    phoneNumber : int = st.text_input("Enter Your Phone Number")
    password : str = st.text_input("Enter Your Password")

    if st.button("Register") :
        if fristName == "" and lastName == "" and age == "" and email == "" and phoneNumber == "" and password == "":
            st.warning("Please fill all fields correctly.")
        else:
            try:
                age : int = int(age)
                phoneNumber : int = int(phoneNumber)

                user_data : AddUser = AddUser(fristName, lastName, age, email, phoneNumber, password) 
                check = user_data.check_user() # ye check kar ry ga ky user pahaly sy to register to nhi hai hai to True aye ga wana false

                if check:
                    st.warning("Please Change Your Email And Password")
                else:
                    push_data : AddUser = user_data.data_send() #  ye database.json main user ko add kary ga. agar user add ho jaye ga to Trye wana false
                    if push_data:
                        st.success("Registered Successfully")
                        # Show a styled success message
                        st.markdown("""
                        <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; background-color: #f0fff0;">
                            <h3 style="color: #2e7d32;">🎉 Welcome to SUK Bank!</h3>
                            <p style="font-size: 16px; color: #333;">
                                Your account has been successfully created.<br><br>
                                💸 You have received <strong style="color: green;">Rs: 100</strong> as a welcome bonus.<br>
                                Enjoy your banking experience with us!
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        time.sleep(18)
                        return(True) 
                    else:
                        st.warning("Somethink Was Wrong Please Check Your Information")
                        return False

            except ValueError as error:
                st.warning("Please Check Your Information Because Your Data is Incorrect.")
                return False