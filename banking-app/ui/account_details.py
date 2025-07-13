import streamlit as st
from backend.find_user_data import  read_curent_user_data
# Custom CSS for card styling
st.markdown("""
    <style>
        .card {
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .card h2 {
            color: #0d6efd;
            margin-bottom: 20px;
        }
        .card p {
            font-size: 18px;
            line-height: 1.6;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)


# # is ky andar user ky account ki sary information aye gi
def Account_details():
    user_data = read_curent_user_data()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Account Details")
    st.write(f"**Frist Name:** {user_data['fristName']}")
    st.write(f"**Last Name:** {user_data['lastName']}")
    st.write(f"**Age:** {user_data['age']}")
    st.write(f"**Phone Number:** {user_data['phoneNumber']}")
    st.write(f"**Password:** {user_data['password']}")
    st.write(f"**Account Number:** {user_data['account']['account_number']}")
    st.write(f"**Account Create:** {user_data['account']['created_at']}")
    st.markdown('</div>', unsafe_allow_html=True)
        
    # Footer
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("© 2025 MyBank. All rights reserved. | Contact Support: SUK@mybank.com")
    st.markdown('</div>', unsafe_allow_html=True)