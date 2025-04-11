from tkinter.simpledialog import askstring
from tkinter import *
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import null
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import mplfinance as mpf
import datetime as dt
import pandas as pd


def getbalanceSheet():

    pd.set_option('display.max_rows', None)#hidden data of row is not hidden anymore
    pd.set_option('display.max_columns', None)#hidden data of column is not hidden anymore

    def closeWindow():
        ui.destroy()

    ui = Tk()
    ui.title('BALANCE SHEET')

    pd.set_option('display.max_rows', None)#hidden data of row is not hidden anymore
    pd.set_option('display.max_columns', None)#hidden data of column is not hidden anymore

    text_widget = tk.Text(ui, height=30, width=80)
    text_widget.pack(pady=10)

    balance_sheet = yf.Ticker(stockName).balance_sheet

    text_widget.insert(tk.END, str(balance_sheet))


    close_button = tk.Button(ui, text="Close", command=closeWindow)
    close_button.pack()

    #print(dividendHistory)

    ui.mainloop()

def getIncomeStatement():

    pd.set_option('display.max_rows', None)#hidden data of row is not hidden anymore
    pd.set_option('display.max_columns', None)#hidden data of column is not hidden anymore

    def closeWindow():
        ui.destroy()

    ui = Tk()
    ui.title('INCOME STATEMENT')

    pd.set_option('display.max_rows', None)#hidden data of row is not hidden anymore
    pd.set_option('display.max_columns', None)#hidden data of column is not hidden anymore

    text_widget = tk.Text(ui, height=30, width=80)
    text_widget.pack(pady=10)

    incomeStatement = yf.Ticker(stockName).incomestmt

    text_widget.insert(tk.END, str(incomeStatement))


    close_button = tk.Button(ui, text="Close", command=closeWindow)
    close_button.pack()

    #print(dividendHistory)

    ui.mainloop()



def getDividendHistory(stockName):

    def closeWindow():
        ui.destroy()

    ui = Tk()
    ui.title('DIVIDEND HISTORY ')

    pd.set_option('display.max_rows', None)#hidden data of row is not hidden anymore
    pd.set_option('display.max_columns', None)#hidden data of column is not hidden anymore

    text_widget = tk.Text(ui, height=10, width=40)
    text_widget.pack(pady=10)

    start_date = dt.datetime.now() - dt.timedelta(days=365)
    df = yf.download(stockName, start=start_date, end=dt.datetime.now(), interval="1wk")
    dividendHistory = yf.Ticker(stockName).get_dividends()


    text_widget.insert(tk.END, str(dividendHistory))


    close_button = tk.Button(ui, text="Close", command=closeWindow)
    close_button.pack()

    #print(dividendHistory)

    ui.mainloop()


def getRecommendation(stockName):

    def close_window():
        root.quit()
        root.destroy()


    try:
        start_date = dt.datetime.now() - dt.timedelta(days=365)

        df = yf.download(stockName, start=start_date, end=dt.datetime.now(), interval="1wk")

        reccomendationSummary = yf.Ticker(stockName).get_recommendations_summary()
        print(reccomendationSummary)

        indexArray = []
        rowColumnArray = []

        # Iterate through rows and columns
        for index, row in reccomendationSummary.iterrows():
        #print("Holder:", index)
            indexArray.append(index)

            for column in reccomendationSummary.columns:

                #print("this is column ",column + ":", row[column])
                rowColumnArray.append(row[column])

        categories = ['STRONG BUY ' , 'BUY ' , 'HOLD' , 'SELL' , 'STRONG SELL']
        value = [rowColumnArray[19] , rowColumnArray[20] , rowColumnArray[21] , rowColumnArray[22] , rowColumnArray[23]]

        # Plotting the bar graph
        fig, ax = plt.subplots()
        ax.bar(categories, value)

        # Adding labels and title
        ax.set_xlabel('----------Categories----------')
        ax.set_ylabel('----------Number of Analyst------------')
        ax.set_title('Bar Graph for next 3 months')

        # Creating a Tkinter window
        root = tk.Tk()
        root.title("Bar Graph")

        plt.bar(categories, value)
        # Adding the matplotlib plot to the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Adding a close button
        close_button = tk.Button(root, text="Close", command=close_window)
        close_button.pack(side=tk.BOTTOM)

        # Display the Tkinter window
        tk.mainloop()

    except Exception as e:
        print('The graph data is currently unavailable for this:', e)


def getMajorShareHoldersDataGraph(stockName):

    def close_window():
        root.quit()
        root.destroy()

    try:
        start_date = dt.datetime.now() - dt.timedelta(days=365)

        df = yf.download(stockName, start=start_date, end=dt.datetime.now(), interval="1wk")

        major_holders_data = yf.Ticker(stockName).get_major_holders()
        print(major_holders_data)
        indexArray = []
        rowColumnArray = []

        # Iterate through rows and columns
        for index, row in major_holders_data.iterrows():
            print("Holder:", index)
            indexArray.append(index)

            for column in major_holders_data.columns:
                print(column + ":", row[column])
                rowColumnArray.append(row[column])

        categories = [indexArray[0], indexArray[1], indexArray[2], indexArray[3]]
        values = [rowColumnArray[0], rowColumnArray[1], rowColumnArray[2], rowColumnArray[3]]

        # Plotting the bar graph
        fig, ax = plt.subplots()
        ax.bar(categories, values)

        # Adding labels and title
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Bar Graph')

        # Creating a Tkinter window
        root = tk.Tk()
        root.title("Bar Graph")

        plt.bar(categories , values)
        # Adding the matplotlib plot to the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Adding a close button
        close_button = tk.Button(root, text="Close", command=close_window)
        close_button.pack(side=tk.BOTTOM)

        # Display the Tkinter window
        tk.mainloop()

    except Exception as e:
        print('The graph data is currently unavailable for this:', e)


def stockNameAskWindow():
    # Create the Tkinter root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Now you can call askstring
    name = askstring("Input", "PLEASE ENTER YOUR SHARE SYMBOL")

    # Once you're done with the dialog, you can destroy the root window
    root.destroy()
    return name

name = stockNameAskWindow()
stockName = name
stockNameToUpper = stockName.upper()



def getNews(newsText, stockName):

    data = yf.Ticker(stockName).get_news()
    newsText.insert(END, "NEWS FOR " + stockName.upper() + ":\n\n", "bold")

    for news_item in data:
        newsText.insert(END, "Title: " + news_item['title'] + "\n")
        newsText.insert(END, "Publisher: " + news_item['publisher'] + "\n")
        newsText.insert(END, "Link: " + news_item['link'] + "\n\n")
        newsText.insert(END, '-------------------------------------------------------------------------------------------'+"\n\n")
    newsText.config(state='disabled')

def financialAnalysisOfTheCompany(FinancialAnalysisText , stockName):

    balance_sheet = yf.Ticker(stockName).balance_sheet
    income_statement = yf.Ticker(stockName).financials

    latest_date = balance_sheet.columns[0]
    # print(balance_sheet)
    # print(income_statement)

    print('CASH FLOW ANALYSIS OF THE COMAPTY')
    print('---------------------------------------------------------------------------------------------------------')

    #print(balance_sheet)

    #current assets f the company
    cash_and_cash_equivalents = balance_sheet.loc['Cash And Cash Equivalents', latest_date]
    accounts_receivable = balance_sheet.loc['Net Receivables', latest_date] if 'Net Receivables' in balance_sheet.index else 0
    inventory = balance_sheet.loc['Inventory', latest_date] if 'Inventory' in balance_sheet.index else 0
    prepaid_assets = balance_sheet.loc['Prepaid Expenses', latest_date] if 'Prepaid Expenses' in balance_sheet.index else 0
    other_current_assets = balance_sheet.loc['Other Current Assets', latest_date] if 'Other Current Assets' in balance_sheet.index else 0
    current_assets = cash_and_cash_equivalents + accounts_receivable + inventory + prepaid_assets + other_current_assets

    #current liabilaities of the comapny
    accounts_payable = balance_sheet.loc['Accounts Payable', latest_date] if 'Accounts Payable' in balance_sheet.index else 0
    current_debt = balance_sheet.loc['Short Long Term Debt', latest_date] if 'Short Long Term Debt' in balance_sheet.index else 0
    other_current_liabilities = balance_sheet.loc['Other Current Liabilities', latest_date] if 'Other Current Liabilities' in balance_sheet.index else 0
    current_liabilities = accounts_payable + current_debt + other_current_liabilities

    #curent ratio
    current_ratio = current_assets / current_liabilities

    #profit margin
    net_income = income_statement.loc['Net Income', latest_date] if 'Net Income' in income_statement.index else 0
    total_revenue = income_statement.loc['Total Revenue', latest_date] if 'Total Revenue' in income_statement.index else 0
    profit_margin = (net_income / total_revenue) * 100 if total_revenue != 0 else 0


    #shareholder equity
    total_shareholders_equity = balance_sheet.loc['Total Stockholder Equity', latest_date] if 'Total Stockholder Equity' in balance_sheet.index else 0

    #roe ca;culation its workin progress
    roe = (net_income / total_shareholders_equity) * 100 if total_shareholders_equity != 0 else 0

    # Total Debt
    total_debt = balance_sheet.loc['Total Debt', latest_date] if 'Total Debt' in balance_sheet.index else 0

    # Total Assets
    total_assets = balance_sheet.loc['Total Assets', latest_date] if 'Total Assets' in balance_sheet.index else 0

    #debt ratoo calcuation
    debt_ratio = (total_debt / total_assets) * 100 if total_assets != 0 else 0


    #Liquidty ratio
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities != 0 else 0
    #cash ratio
    cash_ratio = cash_and_cash_equivalents / current_liabilities if current_liabilities != 0 else 0



    print('financial statements ')
    print('---------------------------------------------------------------------------------------------------------')
    # Revenue
    total_revenue = income_statement.loc['Total Revenue', latest_date] if 'Total Revenue' in income_statement.index else 0

    # Cost of Goods Sold
    cost_of_goods_sold = income_statement.loc['Cost Of Revenue', latest_date] if 'Cost Of Revenue' in income_statement.index else 0

    # Grosss Profit Margin
    gross_profit_margin = ((total_revenue - cost_of_goods_sold) / total_revenue) * 100 if total_revenue != 0 else 0


    operating_income = income_statement.loc['Operating Income', latest_date] if 'Operating Income' in income_statement.index else 0

    # Operating Income Margin
    operating_income_margin = (operating_income / total_revenue) * 100 if total_revenue != 0 else 0


    # Net Income
    net_income = income_statement.loc['Net Income', latest_date] if 'Net Income' in income_statement.index else 0

    # Net Profit Margin
    net_profit_margin = (net_income / total_revenue) * 100 if total_revenue != 0 else 0

    FinancialAnalysisText.insert(END,'-------------------------------------------------------------------------------------------' + "\n\n")
    FinancialAnalysisText.insert(END, "CURRENT RATIO : " + str(current_ratio)+"\n")
    FinancialAnalysisText.insert(END, "PROFIT MARGIN : " + str(profit_margin) + "\n")
    #FinancialAnalysisText.insert(END, "CURRENT RATIO :- " + str(current_ratio) + "\n")
    #print("Return on Equity (ROE):", roe)
    FinancialAnalysisText.insert(END, "DEBT RATIO : " + str(debt_ratio) + "\n")
    FinancialAnalysisText.insert(END, "GROSS PROFIT MARGIN : " + str(gross_profit_margin) + "\n")
    FinancialAnalysisText.insert(END, "OPERATING INCOME MARGIN : " + str(operating_income_margin) + "\n")
    FinancialAnalysisText.insert(END, "NET PROFIT MARGIN : " + str(net_profit_margin) + "\n")
    FinancialAnalysisText.insert(END, '-------------------------------------------------------------------------------------------'+"\n\n")
    FinancialAnalysisText.insert(END,'ANALYSIS RESULT OF THE COMPANY BY OUR SIDE ' + "\n\n")
    FinancialAnalysisText.insert(END, '-------------------------------------------------------------------------------------------'+"\n\n")

    if current_ratio > 1 and profit_margin > 0 and debt_ratio < 50:

        FinancialAnalysisText.insert(END, 'COMPANY IS FUNDAMENTALLY STRONG ' + "\n\n")
       # print('Company is fundamentally strong')

    else :

        FinancialAnalysisText.insert(END ,'COMPANY IS FUNDAMENTALLY WEAK ' + "\n\n")
        #print('company is fundamentally weak ')

def close_window():
    ui.quit()
    ui.destroy()

def latestPrice(stockName):
    try:
        latest_price = yf.Ticker(stockName).history(period='1d')['Close'].iloc[-1]
        # Format the latest price to two decimal places
        latest_price_formatted = "{:.2f}".format(latest_price)
        # Return the formatted latest price as a string
        return str(latest_price_formatted)
    except Exception as e:
        print("Error fetching latest price:", e)
        return "N/A"  # Return "N/A" if there's an error fetching the latest price


ui = Tk()
#getMajorShareHoldersDataGraph(stockName)

# Create a frame to contain the treeview and chart
frame = Frame(ui)
frame.place(x=20, y=140)  # Adjust x and y coordinates as needed

# Create the Treeview widget with three columns
tree = ttk.Treeview(frame, columns=("1", "2", "3"), show="headings", height=30)
tree.heading("1", text="SR.NO")
tree.heading("2", text="COUNTRY NAME")
tree.heading("3", text="EXTENSION")

# Insert sample data into the table
# For example, let's insert some country names and their extensions
country_data = [

    ("India " , ".NS"),
    ("India " , ".BO"),
    ("United States", ".US"),
    ("United Kingdom", ".UK "),
    ("Germany", ".DE"),
    ("Canada", ".CA"),
    ("Australia", ".AU")

]

#geeksforgeeks code
for i, (country, extension) in enumerate(country_data, start=1):
    tree.insert("", tk.END, values=(i, country, extension))


# Set the width of columns
tree.column("1", width=100)
tree.column("2", width=100)
tree.column("3", width=100)

tree.pack(side=LEFT)

# Financial analysis text
FinancialAnalysisText = Text(ui, height=18, width=95)
FinancialAnalysisText.place(x=1110, y=140)
FinancialAnalysisText.tag_configure("bold", font=("Helvetica", 10, "bold"))
FinancialAnalysisText.insert(END, "FUNDAMENTAL ANALYSIS\n\n", "bold")
FinancialAnalysisText.config(state='disabled')
FinancialAnalysisText.config(state='normal')

financialAnalysisOfTheCompany(FinancialAnalysisText, stockNameToUpper)

# News text
newsText = Text(ui, height=20, width=95)
newsText.place(x=1110, y=439)
newsText.tag_configure("bold", font=("Helvetica", 10, "bold"))
newsText.insert(END, "NEWS\n\n ", "bold")
getNews(newsText, stockNameToUpper)

newsText.config(state='disabled')

# Download stock data and create candlestick chart
#candleStick chart , OHLC chart , line chart , Bar chart
start_date = dt.datetime.now() - dt.timedelta(days=10*365)
df = yf.download(stockNameToUpper, start=start_date, end=dt.datetime.now(), interval="1wk")
df.index = pd.to_datetime(df.index)

# Create the Matplotlib figure and plot the candlestick chart
fig, ax = mpf.plot(df, type='candle', volume=True, style='charles', returnfig=True)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack(side=RIGHT)

#ui.configure(bg="your color should come here ")

ui.geometry('1900x1500')
ui.title('FINANCIAL ANALYSIS PLATFORM')

bold_label = tk.Label(ui, text=" COUNTRY EXTENSIONS", font=("Helvetica", 12, "bold"))
bold_label.pack(anchor=W, padx=20, pady=85)  # Anchor to the left, add padding for spacing

addSymbolButton = Button(ui, text="CLOSE PROGRAM", command = lambda :close_window())
addSymbolButton.place(x=20, y=110)

getMajorShareHoldersGraphButton = Button(ui , text = 'VIEW MAJOR SHARE HOLDERS ' , command = lambda: getMajorShareHoldersDataGraph(stockName))
getMajorShareHoldersGraphButton.place(x=20 , y = 770)

getReccomendationButton = Button(ui , text = 'VIEW STOCK RECOMMENDATION ' , command = lambda: getRecommendation(stockName))
getReccomendationButton.place(x = 200 , y = 770)

viewDividendHistoryButton = Button(ui , text = ' VIEW DIVIDEND HISTORY ' , command = lambda : getDividendHistory(stockName))
viewDividendHistoryButton.place(x = 405 , y = 770)

viewBalanceSheetButton = Button(ui , text = 'VIEW BALANCE SHEET ' , command = lambda : getbalanceSheet())
viewBalanceSheetButton.place(x = 570 , y =770)

viewicomeStatement = Button(ui , text = ' VIEW INCOME STATEMENT ' , command = lambda : getIncomeStatement())
viewicomeStatement.place(x = 730 , y = 770)

headingOfStock = stockNameToUpper + " :  " + latestPrice(stockName)

stockNameBoldText = tk.Label(ui, text=headingOfStock, font=("Helvetica", 12, "bold"))
stockNameBoldText.place(x=330, y=110)
#chartCandleStickSymbolButton.place(x=330 , y=110)

chartPatternCombobox = ttk.Combobox(ui, values=["Candle", "OHLC"])  # Add more patterns as needed
chartPatternCombobox.current(0)  # Set default selection
chartPatternCombobox.bind("<<ComboboxSelected>>", null)
chartPatternCombobox.place(x=600, y=110)

#time intervals in yfinance 1d,1wk,1mo,1m
timeIntervalPatternCombobox = ttk.Combobox(ui, values=['1 DAY ', '1 WEEK' , '1 MONTH' , '1 MONTH' , '1 MINUTE'])  # Add more patterns as needed
timeIntervalPatternCombobox.current(0)  # Set default selection
timeIntervalPatternCombobox.bind("<<ComboboxSelected>>", null)
timeIntervalPatternCombobox.place(x=750, y=110)

ui.mainloop()