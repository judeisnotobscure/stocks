from tkinter import *
from tkinter.ttk import Progressbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
from stock_class import Stock
from acct import Robin_trader
from robin_bot import Robin_bot
from functools import partial
import time
from login import Login
import threading
import queue
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
cf.go_offline()

class Stock_analyzer(Tk):
    def __init__(self, master):
        username=""
        password =""
        self.master = master
        self.trader = Robin_trader(username, password)
        self.trader.login()
        # self.trader=Login(self.master)
        # create login check then self.run()
        # if self.trader ==True:
        #     self.run()
        self.run()
    def run(self):
        self.master.title("Stock Analyzer")
        self.bot = Robin_bot(self.trader)
         #colors
        self.bkg = "#555555"
        self.green = '#00c805'
        self.red = '#ff5800'
        self.blue = '#1f98f2'
        self.orange='#f59445'
        self.txt= '#fdfdfd'
        self.menu_bkg='#1E2124'

        ################
        ## Main Containers
        ###############
        #menu
        self.top_frame = Frame(self.master, width = 1000, height = 20, background=self.menu_bkg)
        #canvas
        self.canvas = Frame(self.master, width=1000, height=800, background=self.bkg )
        #frame
        self.side_frame = Frame(self.master, width=400, height=800, background=self.menu_bkg)
        
        #  Layout for main containers
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.top_frame.grid(row=0,columnspan=2, sticky=EW)
        self.canvas.grid(row = 1, column=1, sticky=E)
        self.side_frame.grid(row=1,column=0, sticky = NW)

        # for price
        self.message_price = "Enter a price point"
        self.price_label_text = StringVar()
        self.price_label_text.set(self.message_price)
        self.price_label = Label(self.side_frame, textvariable=self.price_label_text)
        self.price_range_button = Button(self.side_frame, text="Find Good Stocks", command=lambda: self.thread_callback(self.get_stocks), state=DISABLED)
        price_validator = self.master.register(self.validate_price) # we have to wrap the command
        self.price_entry = Entry(self.side_frame, validate="key", validatecommand=(price_validator, '%P'))

        # progress bar
        self.progress_bar = Progressbar(self.side_frame, length = 180, 
            style = 'grey.horizontal.TProgressbar',mode='determinate',orient='horizontal')

        # for ticker
        self.message_ticker = "Enter a ticker symbol"
        self.ticker_label_text = StringVar()
        self.ticker_label_text.set(self.message_ticker)
        self.ticker_label = Label(self.side_frame, textvariable=self.ticker_label_text)
        self.ticker_button = Button(self.side_frame, text="ResearchTicker", command=self.stock_submit)
        self.ticker_var=StringVar()
        self.ticker_var.set('')
        ticker_validator=self.master.register(self.validate_ticker)
        self.ticker_entry = Entry(self.side_frame, validate='key',textvariable=self.ticker_var,validatecommand=(ticker_validator,'%P'))

        # for stock info
        self.info_box_text = StringVar()
        self.info_box_text.set('')
        self.info_box = Label(self.side_frame,textvariable=self.info_box_text,
        justify=LEFT,
        wraplength=350, anchor=W)
       
        ##################
        # Layout #####
        #################
       
        #entries
        self.ticker_label.grid(row=0, column=3, columnspan=2, sticky=N+W+E)
        self.ticker_entry.grid(row=1, column=3, columnspan=2, sticky=N+W+E)
        self.price_label.grid(row=0, column=0, columnspan=2, sticky=N+W+E)
        self.price_entry.grid(row=1, column=0, columnspan=2, sticky=N+W+E)
        self.price_range_button.grid(row=2, column=0,columnspan=2)
        self.ticker_button.grid(row=2, column=3, columnspan=2)
        self.progress_bar.grid(row=3,column=1)

        ####################
        # END of Function
        ####################

    ####################
    # Validator Functions
    ####################
    def validate_price(self, new_text):
        if not new_text: # the field is being cleared
            self.price_range = None
            return True

        try:
            price_range = float(new_text)
            if 0 < price_range <= 9999999:
                self.price_range = price_range
                self.price_range_button.configure(state=NORMAL)
                return True
            else:
                return False
        except ValueError:
            return False

    def validate_ticker(self, new_ticker):
        if not new_ticker:
            self.ticker = None
            return True
        try:
            ticker = new_ticker
            if 0<len(new_ticker)<=5:
                self.ticker = ticker
                self.ticker_button.configure(state=NORMAL)
                return True
            else:
                return False
        except ValueError:
            return False

    ###################
    #  Stock Analysis Functions
    ###################
    def graph_stock_yearly(self, stock_df):
        # styling
        mean_line_style = ':'
        axis_text = dict(horizontalalignment='right', verticalalignment='center',
                  fontsize=12, fontdict={'family': 'monospace'})
        stock_label = self.ticker
        target_price = float(stock_df['20_day_mean'].iloc[-1])
        fig = plt.Figure(figsize=(8,3), dpi = 100, facecolor=self.bkg)
        year = fig.add_subplot(111)
        year.set_xlabel('time[D]')
        year.set_ylabel('$ Dollars')
        year.plot(stock_df['close_price'], self.blue,label='close price')
        year.plot(stock_df['20_day_mean'], self.orange, label = '20 day mean',linestyle=mean_line_style)
        year.plot(stock_df['upper'], self.green, label ='upper bound')
        year.plot(stock_df['lower'], self.red, label ='lower bound')
        year.set_facecolor(self.bkg)
        year.set_title("{} Anual Daily Close  (Last Price: $ {}) (mean= $ {:.2f})".format(self.ticker.upper(), self.get_current_price(), target_price))
        year.legend(loc='upper left',fancybox=True, framealpha=0.5)
        canvas = FigureCanvasTkAgg(fig, master = self.canvas)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0, columnspan=3, pady=4, sticky=NSEW)
       

    def graph_stock_daily(self,stock_df):
        # styling
        mean_line_style = ':'
        stock_label = self.ticker
        mean = float(stock_df['30_min_mean'].iloc[-1])
        fig = plt.Figure(figsize=(8,3), dpi = 100, facecolor=self.bkg)
        day = fig.add_subplot(111)
        day.set_xlabel('time[5min]')
        day.set_ylabel('$ Dollars')
        day.plot(stock_df['close_price'],self.blue,label='close price')
        day.plot(stock_df['30_min_mean'], self.orange,label = '30 min mean',linestyle=mean_line_style)
        day.plot(stock_df['upper'],self.green, label ='upper bound')
        day.plot(stock_df['lower'], self.red,label ='lower bound')
        day.set_facecolor(self.bkg)
        day.set_title("{} Daily 5 Min (Last Price: $ {}) (mean = $ {:.2f})".format(self.ticker.upper(), self.get_current_price(),mean))
        day.legend(loc='upper left',fancybox=True, framealpha=0.5)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1,column=0, columnspan=3, pady=4, sticky=NSEW)

    def create_stock(self):
        stock = self.ticker
        self.stock = Stock(stock)

    def get_current_price(self):
        quote = self.stock.get_price()
        return quote

    def input_stock_yearly(self):    
        stock_df = self.stock.get_historicals()
        return stock_df

    def input_stock_daily(self):
        daily_df = self.stock.get_daily()
        return daily_df

    def display_info(self):
        self.info_box.grid(row=4, column=0, columnspan=4)
        self.stock.get_info()
        description=""
        for key in self.stock.info[0]:
            description=description +"{}: {}\n".format(key, self.stock.info[0][key])
        print(description)
        self.info_box_text.set(description)
        self.info_box.grid(self.side_frame,row=5,column=1,rowspan=3)
        self.progress_bar.stop()
        
        
        

    def stock_submit(self):
        self.create_stock()
        self.graph_stock_yearly(self.input_stock_yearly())
        self.graph_stock_daily(self.input_stock_daily())
        self.display_info()

    def get_stocks(self):
        # progress_bar = Progressbar(self.side_frame, length = 180, style = 'grey.horizontal.TProgressbar')
        # progress_bar['value']=50
        # progress_bar.grid(row=3, column=1)
        stock_list = self.bot.top_stocks(self.price_range)
        self.l = Listbox(self.side_frame)
        for i in range(len(stock_list)):
            self.l.insert(i, stock_list[i])
        self.l.bind('<Double-1>', self.go)
        self.l.grid(row = 4, column = 1, pady = 4)
    
    def go(self,event):
        cs= self.l.curselection()
        #updating lable text to selected option
        self.ticker_var.set(self.l.get(cs))
        self.stock_submit()
    
    #### For Threading
    def thread_callback(self,function):
        self.thread_q = queue.Queue()
        self.new_thread = threading.Thread(target = function)
        self.new_thread.start()
        self.progress_bar.start()
        self.after(100,self.listen_for_result)

    def listen_for_result(self):
        try:
            self.progress_bar.step(25)
            self.res = self.thread_q.get(0)
        except queue.Empty:
            self.after(100,self.listen_for_result)
            

if __name__ == '__main__':
    root = Tk()
    my_gui = Stock_analyzer(root)
    root.mainloop()