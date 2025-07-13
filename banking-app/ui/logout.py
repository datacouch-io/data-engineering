import streamlit as st


# Function to handle logout
def logout():

        # Button for login again
    button_clicked = st.button("🔐 Login Again")

    # Custom CSS to style the button
    st.markdown("""
        <style>
                
                .stApp {
            color: white;
        }
                
        .logout-box {
            background-color: #1a1f2e;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 0 20px rgba(255, 99, 71, 0.2);
            animation: fadeOut 1.5s ease-in-out;
        }

        .logout-box h1 {
            color: #FF6B6B;
            font-size: 32px;
        }

        .logout-box p {
            font-size: 18px;
            color: #ccc;
        }

        .emoji {
            font-size: 50px;
            margin-bottom: 15px;
        }

        @keyframes fadeOut {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }

        .relogin-btn {
            margin-top: 25px;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            transition: background-color 0.3s ease;
            cursor: pointer;
        }

        .relogin-btn:hover {
            background-color: #388E3C;
        }
                
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            transition: 0.3s;
        }
                
        div.stButton > button:first-child:hover {
            background-color: #45a049;
            transform: scale(1.03);
        }
            
        </style>
    """, unsafe_allow_html=True)

        
    # UI Layout
    st.markdown("""
        <div class="logout-box">
            <div class="emoji">👋</div>
            <h1>You’ve been logged out!</h1>
            <p>We hope to see you again soon at <strong>SUK Bank</strong>.</p>
            
        </div>
    """, unsafe_allow_html=True)

    # Action after button click
    if button_clicked:
        st.session_state.display = True  # Show login/register page
        st.rerun()  # Rerun the app