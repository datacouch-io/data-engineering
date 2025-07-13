from dataclasses import dataclass
import json
import streamlit as st
import random
from datetime import datetime

# is ky andar jo user register kary ga us ka fristname is main aye ga phir wo after_log_reg.py main show ho ye ga or fristname nichy st aye ga
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# is ky andar jo user register kary ga us ka password is main aye ga phir wo after_log_reg.py main show ho ye ga or password nichy st aye ga
if "user_password" not in st.session_state:
    st.session_state.user_password = None


## is main auto account number generate hoye gy
def generate_account_number():
    # 14-digit ka account number generate karega
    new_account_number = random.randint(10**13, 10**14 - 1)

    with open("backend/database.json", "r") as file:
        data: list[dict] = json.load(file)
        # Check karega ke number already kisi user ka to nahi
        existing_numbers = {user["account"]["account_number"] for user in data}
        
        # Jab tak unique number nahi milta, dobara generate karo
        while new_account_number in existing_numbers:
            new_account_number = random.randint(10**13, 10**14 - 1)

    return new_account_number

@dataclass
class AddUser(object):
    fristName : str
    lastName : str
    age : int
    email : str
    phoneNumber : int
    password : str


#    is main user ko check kar rah ho ky wo pahary sy to login nhi hai
    def check_user(self) -> bool:
        try:
            with open("backend/database.json", "r") as file:
                data : list[dict] = json.load(file)
            
                find = list(filter(lambda x : x["email"] == self.email and x["password"] == self.password , data))
                if find :
                    return True
                else :
                    return False

        except Exception as e:
            print("Error saving data:", e)
            return False

#   ye user ko database.json main add karry ga
    def data_send(self) -> bool:
        dataSchema : list[dict] = [
            {
                "fristName" : self.fristName,
                "lastName" : self.lastName,
                "age" : self.age,
                "email" : self.email,
                "phoneNumber" : self.phoneNumber,
                "password" : self.password,
                "account":{
                    "account_number": generate_account_number(), # is main user ka account number generate hoye ga
                    "created_at": f"{datetime.now().strftime('%Y-%m-%d')}", # is main current date aye gi
                    "balance": 100,
                    "transactions":[]
                }   
            }
        ]

        try:
            with open("backend/database.json", "r") as file:
                old_data : list[dict] = json.load(file)

                for i in old_data:
                    dataSchema.append(i)

            with open("backend/database.json", "w") as file:
                json.dump(dataSchema, file, indent=4)
            st.session_state.user_name = self.fristName # user ka frist name jaraha hai
            st.session_state.user_password = self.password # user ka password jaraha hai
            return True
        except Exception as e:
            print("Error saving data:", e)
            return False
        
