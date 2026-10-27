from datetime import datetime
import json
import os
from enum import IntEnum
class Transaction:
    def __init__(self,amount:float,category:str,type:str,date:datetime=None,id:int = None):
        if type.lower().strip() not in ["income","expense"]:
            raise ValueError("It can just come in or go out nothing else!")
        if amount <= 0:
            raise ValueError("Amount must be bigger than 0")
        self.amount:float = amount
        self.category:str = category
        self.type:str = type.lower().strip()
        self.date:datetime =date if date is not None else datetime.now()
        self.id : int = id
        
    def __str__(self):
        cleanDate = self.date.strftime("%Y-%m-%d %H:%M")
        return f"Category:{self.category}||Type:{self.type}||Amount:{self.amount}||Date:{cleanDate}||ID:{self.id}"
    def __eq__(self, value):
        if not isinstance(value, Transaction):
            return False
        return self.id == value.id
    def __repr__(self):
        return self.__str__()
    def to_dict(self):
        return {
        "id": self.id,
        "amount": self.amount,
        "category": self.category,
        "type": self.type,
        "date": self.date.strftime("%Y-%m-%d %H:%M")  
    }
class Account:
    def __init__(self,mail:str):
        self.mail = mail
        self.log = dict()
        self._balance:float = 0.0
        
    @property
    def balance(self):
        return self._balance
    def add_transaction(self,action:Transaction):
        if action.type == "income":
            self._balance +=action.amount
        else:
            self._balance-=action.amount
        nextID : int = len(self.log) + 1
        action.id=nextID
        self.log[nextID]=action
        
        
    def FilterbyType(self,user_type:str):
        if user_type.lower().strip() == "income":
            return [value for value in self.log.values() if value.type == "income"]
        elif user_type.lower().strip() == "expense":
            return [value for value in self.log.values() if value.type == "expense"]
        return []
        
        
    def FilterbyAmount(self,user_amount:float,relation:str):
        match relation.lower().strip():
            case "bigger":
                return [value for value in self.log.values() if value.amount > user_amount]
            case "smaller":
                return [value for value in self.log.values() if value.amount < user_amount]
            case "equal":
                return [value for value in self.log.values() if value.amount == user_amount]
            case _: return []
                
    def FilterbyCategory(self,user_category:str):
        return [value for value in self.log.values() if value.category.lower().strip() == user_category.lower().strip()]
    
    
    def FilterbyDate(self,user_date:datetime,relation:str):
        match relation.lower().strip():
            case "bigger":
                return [value for value in self.log.values() if value.date > user_date]
            case "smaller":
                return [value for value in self.log.values() if value.date < user_date]
            case "equal":
                return [value for value in self.log.values() if value.date.date() == user_date.date()]        
            case _: return []
    def to_dict(self):
        return{
            "mail" : self.mail,
            "balance" : self.balance,
            "log" : {Id : log.to_dict() for Id,log in self.log.items()}
        }
    def __str__(self):
        if not self.log:
            return f"({self.mail}): No transaction yet"
        
        head = f"--- {self.mail} Transactions (Balance: {self.balance} TL) ---\n"
        lines = "\n".join(str(value) for value in self.log.values())
        return head + lines
            
    def __len__(self):
        return len(self.log)
    
def save_account(account : Account):
    fileName = f"{account.mail}.json"
    with open (fileName,"w",encoding="utf-8") as f:
        json.dump(account.to_dict(),f,indent = 4)
        
def load_account(mail : str):
    fileName = f"{mail}.json"
    with open (fileName,"r") as f:
        data = json.load(f)
    account = Account(data["mail"])
    for item in data["log"].values():
        date_obj = datetime.strptime(item["date"], "%Y-%m-%d %H:%M")
        transactions = Transaction(
        amount=item["amount"],
        category=item["category"],
        type=item["type"],
        date=date_obj,
        id=item["id"]
    )
        account.add_transaction(transactions)
    return account
class Menu(IntEnum):
    Add_transaction = 1
    List_transactions = 2
    Filter_transactions = 3
    Exit_menu = 4
    def show_menu():
        for option in Menu:
            print(f"{option.name} = {option.value}")
class Filter_Menu(IntEnum):
    FilterbyAmount = 1
    FilterbyCategory = 2
    FilterbyType = 3
    FilterbyDate = 4
    Exit = 5
    def show_filter_menu():
        for option in Filter_Menu:
            print(f"{option.name} = {option.value}")
            
    
def main():
    email:str = input("Welcome to transactions portal please enter your e-mail adress: ")
    fileName:str=f"{email}.json"
    if os.path.exists(fileName):
        print(f"Welcome {email} your account is loading")
        account = load_account(email)
    else:
        account = Account(email)
        print(f"Welcome {email} your account has been estabished")
    while True:
        Menu.show_menu()
        try:
            choice = int(input("Please enter your choice(1-4): "))
        except ValueError:
            print("Please enter a number in (1-4)interval!")
            continue
        match(choice):
            case Menu.Add_transaction:
                try:
                    amount:float = float(input("Enter transactions amount:"))
                    category:str= input("Enter transactions category:").strip()
                    type:str = input("Enter transactions type:").strip()
                    new_transaction = Transaction(amount,category,type)
                    account.add_transaction(new_transaction)
                    print("add_transaction was sucessful")
                except ValueError as e:
                    print(f"Wrong input {e} turning back to beginning")
            case Menu.List_transactions:
                print(f"Length of transactions: {len(account)}")
                print(account)
            case Menu.Filter_transactions:
                while True:
                    Filter_Menu.show_filter_menu()
                    try:
                        filter_choice:int = int(input("Which filter would you like to apply?(1-5) "))
                    except ValueError as e:
                        print(f"Wrong input {e} turning back to beginning")
                        continue
                    match (filter_choice):
                        case Filter_Menu.FilterbyAmount:
                            try:
                                user_amount:float = float(input("Write the amount you would like to compare"))
                                relation : str = input("Write the relation between user amount and amount ")
                            except ValueError as e:
                                print(f"Wrong input {e} turning back to beginning")
                                continue
                            print(account.FilterbyAmount(user_amount,relation))
                        case Filter_Menu.FilterbyCategory:
                            try:
                                user_category:str =input("Write the category you would like to filter")
                            except ValueError as e:
                                print(f"Wrong input {e} turning back to beginning")
                                continue
                            print(account.FilterbyCategory(user_category))
                        case Filter_Menu.FilterbyType:
                            try:
                                user_type:str = (input("Write the type you would like to filter"))
                            except ValueError as e:
                                print(f"Wrong input {e} turning back to beginning")
                                continue
                            print(account.FilterbyType(user_type))
                        case Filter_Menu.FilterbyDate:
                            str_date = input("Enter the date you would like to filter YYYY-AA-GG, z.B: 2026-09-20): ")
                            try:
                                user_date:datetime = datetime.strptime(str_date,"%Y-%m-%d")
                                relation_date : str = input("Write the relation between user date and date ")
                            except ValueError as e:
                                print(f"Wrong input {e} turning back to beginning")
                                continue
                            print(account.FilterbyDate(user_date,relation_date))
                        case Filter_Menu.Exit:
                            print("Exiting filter menu")
                            break       
                        case _:
                            print("Invalid option, please choose between 1 and 5!")
            case Menu.Exit_menu:
                save_account(account)
                print(f"\nAll transactions saved to {account.mail}.json Good bye!")
                break
            case _:
                print("Invalid option, please choose between 1 and 4!")
main()
        
    
        
    
    
    
    
    


        
        
        
    
        