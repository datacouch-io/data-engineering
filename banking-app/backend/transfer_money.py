from dataclasses import dataclass
from backend.find_user_data import read_curent_user_data
import json
from datetime import datetime
from typing import Union

@dataclass
class TransferMoney:
    account_number : int
    amount : int
    description : str

    ## is ky andar jo current hai us ky data ko handle kar raha hai
    def current_account(self) -> Union[bool, str]:
        ## ye schema hai or is main current user ny jo transfer kia hai us ka data is main araha hai
        current_user_transfer_schema = {
            "type": "debit",
            "amount" : self.amount,
            "description": self.description,
            "to_account" : self.account_number,
            "transfer_date": f"{ datetime.now().strftime('%Y-%m-%d')}",
            "transfer_time": f"{  datetime.now().strftime('%H:%M:%S')}"
        }
        ## is ky andar jo current ka data araha hai or ye data bankend/find_user_data.py sy araha hai
        curent_user_data = read_curent_user_data()

        ## is ky andar update howa data aye ga
        dataSchema : list[dict] = []

        try:
            with open("backend/database.json", "r") as file:
                old_data : list[dict] = json.load(file)
                ## is ky andar check kar raha ho ky jo account number araha hai wo account number database.json main hai ya nhi
                find_transfer_user_accound = list(filter(lambda x : x["account"]["account_number"] == self.account_number, old_data))
                if find_transfer_user_accound: ## agar database.json main account number hoye ga to ye chaly ga
                    for i in old_data:
                        ## is main check kar raha ho ky database.json main sy current user ka data li kar raha ho or us data ko change kar raha ho
                        if i["account"]["account_number"] == curent_user_data["account"]["account_number"]:
                            if i["account"]["balance"] >= self.amount: ## current user ny jo amount dia hai us ky account main utny pasy hai 
                                i["account"]["balance"] -= self.amount ## current user ky account sy amount minus kar raha ho
                                i["account"]["transactions"].append(current_user_transfer_schema) ## is ky andar current_user_transfer_schema current user ny jo transfer kia hai us ka data jaraha hai
                                dataSchema.append(i)
                            else:
                                return "You don't have balance in your account."
                        else:
                            dataSchema.append(i)
                else:
                    return "This account was not found"

            ## database.json main update data save ho raha hai
            with open("backend/database.json", "w") as file:
                json.dump(dataSchema, file, indent=4)
            return True
        except Exception as e:
            print("Error saving data:", e)
            return False
        


    def transfer_account(self) -> Union[str, bool]:
        ## is ky andar jo current ka data araha hai or ye data bankend/find_user_data.py sy araha hai
        curent_user_data = read_curent_user_data()

        ## ye schema hai or is main current user ny jo transfer kia hai us ka data is main araha hai
        transfer_user_schema = {
            "type": "credit",
            "amount" : self.amount,
            "description": self.description,
            "to_account" : curent_user_data["account"]["account_number"],
            "transfer_date": f"{ datetime.now().strftime('%Y-%m-%d')}",
            "transfer_time": f"{  datetime.now().strftime('%H:%M:%S')}"
        }
      

        ## is ky andar update howa data aye ga
        dataSchema : list[dict] = []

        try:
            with open("backend/database.json", "r") as file:
                old_data : list[dict] = json.load(file)
                for i in old_data:
                    ## is main check kar raha ho ky database.json main sy current user ka data li kar raha ho or us data ko change kar raha ho
                    if i["account"]["account_number"] == self.account_number:
                        i["account"]["balance"] += self.amount ## current user ky account sy amount minus kar raha ho
                        i["account"]["transactions"].append(transfer_user_schema) ## is ky andar transfer_user_schema current user ny jo transfer kia hai us ka data jaraha hai
                        dataSchema.append(i)
                    else:
                        dataSchema.append(i)
            
            ## database.json main update data save ho raha hai
            with open("backend/database.json", "w") as file:
                json.dump(dataSchema, file, indent=4)
            return True
        except Exception as e:
            print("Error saving data:", e)
            return False
