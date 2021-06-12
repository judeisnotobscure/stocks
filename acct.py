# Robin Trader Class
import robin_stocks as r
import pandas as pd
import matplotlib.pyplot as plt
from stock_class import Stock

class Robin_trader:
    def __init__(self,username, password):
        self.username = username
        self.password = password
        #self.buying_power
        #self.account
        #self.buying_power
        #self.acct_data_df
        #self.positions
        

    def login(self):  
        #perform account login to Robinhood
        login = r.login(self.username, self.password)
        self.account = r.profiles.load_account_profile(info=None)

    def get_buying_power(self):
        # Returns buying power dollars in float
        self.acct_data_df = pd.DataFrame.from_dict(self.account['margin_balances'], orient= 'index')
        
        cash = self.acct_data_df.loc['unallocated_margin_cash'].tolist()
        self.buying_power = float(cash[0])
        return self.buying_power

    def get_positions(self):
        positions = r.account.build_holdings(with_dividends=False)
        self.positions = pd.DataFrame(positions)
        
        return self.positions

if __name__ == "__main__":  
     
    josh = Robin_trader(username, password)
    josh.login()
    print(josh.get_buying_power())
     
    aapl = Stock("aapl")
    # print(aapl.get_historicals().head())

    
    aapl.get_info()