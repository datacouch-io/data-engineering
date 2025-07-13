# is ko login.py ky andar di a hai
from dataclasses import dataclass
import json
import streamlit as st

# is ky andar jo user register kary ga us ka fristname is main aye ga phir wo after_log_reg.py main show ho ye ga or fristname nichy st aye ga
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# is ky andar jo user register kary ga us ka password is main aye ga phir wo after_log_reg.py main show ho ye ga or password nichy st aye ga
if "user_password" not in st.session_state:
    st.session_state.user_password = None


# ye check kar raha hai ky user register hai ya nhi
@dataclass
class CheckUser(object):
    fristName : str
    lastName : str
    email : str
    password : str

    def check_user(self) -> bool:
        try:
            with open("backend/database.json", "r") as file:
                data : list[dict] = json.load(file)

                find = list(filter(lambda x : x["email"] == self.email and x["password"] == self.password , data))
                if find :
                    st.session_state.user_name = self.fristName # user ka frist name jaraha hai
                    st.session_state.user_password = self.password
                    return True
                else :
                    return False
              
        except Exception as e:
            print("Error saving data:", e)
            return False

  