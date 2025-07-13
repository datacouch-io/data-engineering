import streamlit as st
import json

def find_user_data() -> None:
    user_password = st.session_state.get("user_password", "password") ## is ky andar user ka password araha hai or wo password bankend/add_user.py or bankend/check_user.py sy araha hai 

    with open("backend/database.json", "r") as file:
        data : list[dict] = json.load(file)

        find_user_data = list(filter(lambda x: x["password"] == user_password, data))
        if find_user_data:
            # return find_user_data[0]  ## [0] is liye di hai q ky data array ky andar araha hai
            with open("backend/current_user_data.json", "w") as file:
                push_data = json.dump(find_user_data, file, indent=4)
        else:
            return {
            "user_id": "None",
            "first_name": "None",
            "last_name": "None",
            "age": 00,
            "email": "None",
            "phone_number": 000000000,
            "password": "None",
            "account": {
                "account_number": 0000000000,
                "created_at": 00-00-00,
                "balance": 0.0,
                "transactions": []
        }
    }
                        

def read_curent_user_data() -> dict:
    with open("backend/current_user_data.json", "r") as file:
        data = json.load(file)
        return data[0]