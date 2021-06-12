from tkinter import *
from acct import Robin_trader
import robin_stocks as r

""" Returns Robin_trader object to main for login"""
class Login:
    def __init__(self, master):
        self.master= master

        self.master.geometry('400x150')
        self.master.title("Stock Analyzer Robinhood Login")
        # username 
        self.username_lable = Label(self.master, text="User Name")
        self.username_var = StringVar()
        username_validator = self.master.register(self.validate_user)
        self.username_entry = Entry(self.master, textvariable=self.username_var, validatecommand=(username_validator,'%P'))

        # password
        self.password_label = Label(self.master, text="Password")
        self.password_var = StringVar()
        password_validator= self.master.register(self.validate_password)
        self.password_entry = Entry(self.master, textvariable=self.password_var, show='*', validatecommand=(password_validator,'%P'))

        # login button
        self.button = Button(self.master, text="Login", command =self.login, state=DISABLED)

        # Layout
        self.username_lable.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)
        self.button.grid(row=3, column=0)    

    def validate_user(self, new_text):
        if not new_text:
            self.username = None
            return True
        try:
            if 0<len(new_text)<20:
                self.username = new_text
                self.button.configure(state=NORMAL)
                print(new_text,' is the username')
                return True
            else:

                return False
        except ValueError:
            return False
    
    def validate_password(self, new_text):
        if not new_text:
            self.password = None
            return True
        try:
            if 0<len(new_text)<20:
                self.password = new_text
                self.button.configure(state=NORMAL)
                return True
            else:
                return False
        except ValueError:
            return False

    def login(self):
        self.trader = Robin_trader(self.username, self.password)
        return self.trader