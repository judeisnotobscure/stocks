from stock_class import Stock
from acct import Robin_trader
from scipy.optimize import minimize
import numpy as np
import pandas as pd
from yahoo_fin import options as o
import robin_stocks as r

class Robin_bot():
    def __init__(self,trader):
        self.trader = trader
        self.stock_list=[]
        # self.positions = self.trader.get_positions()

        

    def create_stocks(self):
        for stock in self.positions.columns:
            self.stock =Stock(stock)
            
        

    def suggest_sell(self,stock):
        pass

    def suggest_hold(self,stock):
        pass

    def suggest_buy(self,stock):
        pass
    
    def get_total_value(self):
        #Returns total value of portfolio 
            total = 0
            try:
                for stock in self.portfolio:
                    total += stock[2]
                print(total)
                self.portfolio_toal= total
                return total
            except AttributeError:
                self.build_portfolio()
                self.get_total_value()
                
            
    def build_portfolio(self):
        # returns list of tupples (ticker, shares, $ invested)
        self.portfolio = self.trader.get_positions()
        quant = self.portfolio[self.portfolio.index=='quantity']
        tally = []
        final = []
        for stock in quant.columns:
            quantity= float(quant[stock])
            tally.append((stock,quantity))
        for stock in tally:
            nums=Stock(stock[0])
            price = float(nums.get_price())
            final.append((stock[0],stock[1],stock[1]*price))
        self.portfolio = final
        return final

        
    def top_stocks(self, target_price):
        low_target = target_price*0.7
        high_target = target_price*1.2
        top_hundo= r.markets.get_top_100(info=None)
        top_hundo = pd.DataFrame(top_hundo)
        top_hundo['previous_close']=pd.to_numeric(top_hundo['previous_close'])
        top_hundo_trimmed = top_hundo[(top_hundo['previous_close']> low_target) & (top_hundo['previous_close']<high_target)]
        top_stocks = top_hundo_trimmed['symbol'].to_list()
        return top_stocks

    # def get_rel_vol_sr(self,weights):
        # weights= np.array(weights)
        # ret = np.sum(log_ret.mean()*weights*252)
    
        
    # def analyze_stocks(self):
    #     if self.positions!= True:  
    #         self.positions=self.trader.get_positions()
    #     for stock in self.positions.columns:
    #         stock = Stock(stock)
    #         stock_df = stock.get_historicals()
    #         print(stock_df.head())

if __name__=='__main__':
    username=""
    password=""
    josh = Robin_trader(username, password)
    josh.login()

    bot=Robin_bot(josh)
    
    
    bot.get_total_value()
    print(bot.top_stocks(10))
