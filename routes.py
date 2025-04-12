import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db
import yfinance as yf
import matplotlib.pyplot as plt
import os
from flask import jsonify
import requests

# Create Blueprint for the main routes
main = Blueprint('main', __name__)

NEWS_API_KEY = "3db8fcc3c31e405492f6849159dad9e6"  # Sign up at https://newsapi.org

@main.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Fetch the user by ID
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return "User deleted successfully!", 200
    return "User not found!", 404


@main.route('/admin/view_users')
def view_users():
    # Fetch all users from the database
    users = User.query.all()
    return render_template('view_users.html', users=users)



# Route for login
@main.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        # If the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hashing the password with pbkdf2:sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Storing user info in the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))

    return render_template('signup.html')

# @main.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         # Storing user info in the database without hashing
#         new_user = User(username=username, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#
#         flash('Your account has been created!', 'success')
#         return redirect(url_for('main.login'))
#
#     return render_template('signup.html')



# Route for logout
@main.route('/logout')
@login_required  # Ensure the user must be logged in to access this route
def logout():
    print('user getting logged out ......')
    logout_user()  # Logs the user out
    return redirect(url_for('main.login'))  # Redirect to the login page after logout

# Protected route for logged-in users
@main.route('/index')
@login_required
def index():
    return render_template('index.html')















# Route for fetching news (ensure it's only defined once)
@main.route('/get_news', methods=['POST'])
def get_news():
    stock_symbol = request.form.get('stock_name', '').strip()

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400

    news_data = fetch_news(stock_symbol)

    return render_template('news.html', stock_name=stock_symbol.upper(), news_data=news_data)

# Route for fetching dividends (ensure it's only defined once)
@main.route('/get_dividends', methods=['POST'])
def get_dividends():

    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {

        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"

    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    dividend_data = fetch_dividends(stock_name)
    return render_template('dividend.html', stock_name=stock_name, dividend_data=dividend_data)

# Route for fetching balance sheet (ensure it's only defined once)
@main.route("/get_balanceSheet", methods=['POST'])
def get_balanceSheet():

    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    fetchBalanceSheet = fetch_balanceSheet(stock_name)
    return render_template('balanceSheet.html' , stock_name = stock_name , balanceSheetDict = fetchBalanceSheet)


@main.route('/get_Income_Statement', methods=['POST'])
def get_IncomeStatements():
    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    fetch_IncomeStatements = fetch_Income_Statements(stock_name)
    return render_template('income_statement.html', stock_name=stock_name, incomeStatementDict=fetch_IncomeStatements)

@main.route("/get_stock_recommendation", methods=['POST'])
def get_stock_recommendation():
    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"
    print(stock_name)  # Will output in the format tcs.ns
    # Add your logic to handle `stock_name` here

    categories, values = fetch_StockRecommendation(stock_name)
    return render_template(
        'stockRecommendation.html',
        stock_name=stock_name,
        categories=categories,
        values=values
    )


@main.route("/Financial_Analysis", methods=['POST'])
def get_Financial_Analysis():
    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    print(f"Processing Financial Analysis for stock: {stock_name} (Country: {stock_extension})")

    try:
        # Fetch financial analysis
        analysis_data = fetch_FinancialAnalysis(stock_name)
        if analysis_data is None:
            return f"Could not load financial analysis for {stock_name}.", 500

        (
            total_revenue, cost_of_goods_sold, gross_profit_margin,
            operating_income_margin, operating_income, net_income,
            net_profit_margin, result
        ) = analysis_data

        categories, values = fetch_majorShareHoldersCount(stock_name)
        if categories is None or values is None:
            categories, values = [], []

        latestPrice = latest_price(stock_name) or "N/A"

        fast_info = fetch_fastInfo(stock_name)
        if fast_info is None:
            day_high = day_low = fifty_day_average = market_cap = xAxis = yAxis = priceHike = currency = "N/A"
        else:
            (
                day_high, day_low, fifty_day_average, market_cap,
                xAxis, yAxis, priceHike, currency
            ) = fast_info

        return render_template(
            'fundamental_Analysis.html',
            latestPrice=latestPrice,
            total_revenue=total_revenue,
            cost_of_goods_sold=cost_of_goods_sold,
            gross_profit_margin=gross_profit_margin,
            operating_income=operating_income,
            operating_income_margin=operating_income_margin,
            net_income=net_income,
            net_profit_margin=net_profit_margin,
            result=result,
            stock_name=stock_name,
            categories=categories,
            values=values,
            xAxis=xAxis,
            yAxis=yAxis,
            day_high=day_high,
            day_low=day_low,
            fifty_day_Average=fifty_day_average,
            market_cap=market_cap,
            currency=currency
        )
    except Exception as e:
        print(f"Error encountered: {e}")
        return "Internal Server Error: Unable to process request.", 500


@main.route("/Buy_And_sell_Signals" , methods = ['POST'])

def get_BuySellSignals():

    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    buySellSignals = getTechnicalBuyAndSellSignals(stock_name)
    return render_template('TechnicalAnalysis.html', stock_name=stock_name,
                           BuySellSignalsAnalysis=getTechnicalBuyAndSellSignals)
















def latest_price(stock_name):
    try:
        latest_price = yf.Ticker(stock_name).history(period='1d')['Close'].iloc[-1]
        # Format the latest price to two decimal places
        latest_price_formatted = "{:.2f}".format(latest_price)
        # Return the formatted latest price as a string
        return str(latest_price_formatted)
    except Exception as e:
        print("Error fetching latest price:", e)
        return "N/A"  # Return "N/A" if there's an error fetching the latest price




import yfinance as yf

def fetch_news(stock_name):
    """Fetch stock-related news using NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={stock_name}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        news_data = response.json()

        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            formatted_news = []

            for article in articles[:10]:  # Limit to 10 news articles
                formatted_news.append({
                    "title": article.get("title", "No Title"),
                    "providerPublishTime": article.get("publishedAt", "Unknown Date"),
                    "publisher": article.get("source", {}).get("name", "Unknown Source"),
                    "summary": article.get("description", "No summary available."),
                    "link": article.get("url"),
                    "image": article.get("urlToImage", "")
                })
            return formatted_news
        else:
            return []

    except Exception as e:
        print("Error fetching news:", e)
        return []

def fetch_dividends(stock_name):
    try:
        data = yf.Ticker(stock_name).dividends
        dividend_data = data.to_dict()
        return dividend_data
    except Exception as e:
        return str(e)

def fetch_balanceSheet(stock_name):
    try:
        balanceSheet = yf.Ticker(stock_name).balance_sheet
        balanceSheetData = balanceSheet.to_dict()
        return balanceSheetData
    except Exception as e:
        return str(e)

def fetch_Income_Statements(stock_name):
    try:
        incomeStatementsData = yf.Ticker(stock_name).income_stmt
        incomeStatementDict = incomeStatementsData.to_dict()
        return incomeStatementDict
    except Exception as e:
        return str(e)


def fetch_StockRecommendation(stock_name):
    try:
        reccomendationData = yf.Ticker(stock_name).recommendations

        rowColumn_Array = []

        for index, row in reccomendationData.iterrows():
            for column in reccomendationData.columns:
                rowColumn_Array.append(row[column])

        # Prepare data for Chart.js
        categories = ['STRONG BUY ', 'BUY ', 'HOLD', 'SELL', 'STRONG SELL']
        values = [
            rowColumn_Array[19],
            rowColumn_Array[20],
            rowColumn_Array[21],
            rowColumn_Array[22],
            rowColumn_Array[23]
        ]

        return categories, values
    except Exception as e:
        return str(e), []


def fetch_majorShareHoldersCount(stock_name):

    #graph_path = os.path.join('static', 'Major_Share_Holder_Count_Graph.png')
    try:
        major_shareholder_Count_data = yf.Ticker(stock_name).get_major_holders()
        index_Array = []
        rowColumn_Array = []

        for index, row in major_shareholder_Count_data.iterrows():
            # print("Holder:", index)
            index_Array.append(index)

            for column in major_shareholder_Count_data.columns:
                # print("this is column ",column + ":", row[column])
                rowColumn_Array.append(row[column])

        categories = [index_Array[0], index_Array[1], index_Array[2], index_Array[3]]
        values = [rowColumn_Array[0], rowColumn_Array[1], rowColumn_Array[2], rowColumn_Array[3]]


        return categories , values

    except Exception as e:
        return str(e), []


def fetch_FinancialAnalysis(stock_name):

    try :

        balance_sheet = yf.Ticker(stock_name).balance_sheet
        income_statement = yf.Ticker(stock_name).financials

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


        total_revenue
        cost_of_goods_sold
        gross_profit_margin
        operating_income_margin
        operating_income
        net_income
        net_profit_margin



        if current_ratio > 1 and profit_margin > 0 and debt_ratio < 50:

           result = f"{stock_name.upper()}Share Seems to be Fundamentally Strong according to Our Analysis "




        else :

            result = 'Company seems Fundamentally Weak More Analysis Should be Executed '

        return total_revenue , \
            cost_of_goods_sold , \
            gross_profit_margin , \
            operating_income_margin , \
            operating_income , \
            net_income , \
            net_profit_margin , \
            result

    except Exception as e :

        print('Could not load the details Due to error : {e}')

def fetch_fastInfo(stock_name):
    # Fetch fast_info for the ticker
    operation = yf.Ticker(stock_name).fast_info

    print(operation)

    # Access and print the 'dayHigh' value
    if 'dayHigh' and 'dayLow' and 'fiftyDayAverage' and 'marketCap' and 'quoteType' and 'yearChange' in operation:
        day_high = operation['dayHigh']
        day_low = operation['dayLow']
        fifty_day_average = operation['fiftyDayAverage']
        market_cap = operation['marketCap']
        year_high = operation['yearHigh']
        year_low = operation['yearLow']
        currency = operation['currency']

        xAxis = ['yearhigh', 'yearlow']
        yAxis = [year_high, year_low]

        # calculation profiit for percent return in yaer
        priceHike = ((year_high - year_low) / year_high) * 100

    else:
        print("Key 'dayHigh' not found in fast_info.")


    return  day_high,\
            day_low, \
            fifty_day_average,\
            market_cap, \
            xAxis,\
            yAxis ,\
            priceHike,\
            currency



def getTechnicalBuyAndSellSignals(stock_name):

    # import yfinance as yf
    # import pandas as pd
    # import numpy as np
    # import matplotlib.pyplot as plt
    #
    # # Fetch stock data
    # def get_stock_data(stock_symbol, interval='1h', period='5d'):
    #     try:
    #         data = yf.download(tickers=stock_symbol, interval=interval, period=period)
    #         data.reset_index(inplace=True)
    #         data.rename(columns={'Datetime': 'Datetime', 'Close': 'Close'}, inplace=True)
    #         return data
    #     except Exception as e:
    #         print(f"Error fetching stock data: {e}")
    #         return None
    #
    # # Identify support and resistance
    # def calculate_support_resistance(data):
    #     data['Support'] = np.nan
    #     data['Resistance'] = np.nan
    #     for i in range(1, len(data) - 1):
    #         if data['Close'].iloc[i] < data['Close'].iloc[i - 1] and data['Close'].iloc[i] < data['Close'].iloc[i + 1]:
    #             data.loc[data.index[i], 'Support'] = data['Close'].iloc[i]
    #         if data['Close'].iloc[i] > data['Close'].iloc[i - 1] and data['Close'].iloc[i] > data['Close'].iloc[i + 1]:
    #             data.loc[data.index[i], 'Resistance'] = data['Close'].iloc[i]
    #     return data
    #
    # # Add advanced technical indicators
    # def add_indicators(data):
    #     delta = data['Close'].diff()
    #     gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    #     loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    #     rs = gain / loss
    #     data['RSI'] = 100 - (100 / (1 + rs))
    #     data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    #     data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    #     data['MACD'] = data['EMA_12'] - data['EMA_26']
    #     data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    #     data['BB_Mid'] = data['Close'].rolling(window=20).mean()
    #     data['BB_Upper'] = data['BB_Mid'] + 2 * data['Close'].rolling(window=20).std()
    #     data['BB_Lower'] = data['BB_Mid'] - 2 * data['Close'].rolling(window=20).std()
    #     data['ATR'] = data['High'] - data['Low']
    #     return data
    #
    # # Detect patterns
    # def detect_patterns(data):
    #     data['Pattern'] = ''
    #     for i in range(2, len(data) - 2):
    #         if data['Close'].iloc[i - 2] < data['Close'].iloc[i - 1] > data['Close'].iloc[i] and \
    #                 data['Close'].iloc[i + 1] < data['Close'].iloc[i] > data['Close'].iloc[i + 2]:
    #             data.loc[i, 'Pattern'] = 'Head and Shoulders Top'
    #         if data['Close'].iloc[i - 2] > data['Close'].iloc[i - 1] < data['Close'].iloc[i] and \
    #                 data['Close'].iloc[i + 1] > data['Close'].iloc[i] < data['Close'].iloc[i + 2]:
    #             data.loc[i, 'Pattern'] = 'Inverse Head and Shoulders'
    #     return data
    #
    # # Generate buy/sell signals
    # def generate_signals(data, profit_threshold=0.015, stop_loss_threshold=0.007):
    #     """
    #     Generates buy and sell signals based on multiple indicators.
    #     """
    #     data['Signal'] = 0  # Default: Hold
    #     buy_price = None  # Track the buy price for sell conditions
    #
    #     for i in range(1, len(data)):
    #
    #         # Generate buy signal
    #         if buy_price is None:
    #             if (data['RSI'].iloc[i] < 35 and data['Close'].iloc[i] <= data['Support'].iloc[i]) or \
    #                     (data['Pattern'].iloc[i] == 'Inverse Head and Shoulders'):
    #                 buy_price = data['Close'].iloc[i]
    #                 data.loc[i, 'Signal'] = 1  # Buy signal
    #         else:
    #             # Generate sell signals
    #             current_price = data['Close'].iloc[i]
    #             if current_price >= buy_price * (1 + profit_threshold):  # Profit-taking
    #                 data.loc[i, 'Signal'] = -1
    #                 buy_price = None
    #             elif current_price <= buy_price * (1 - stop_loss_threshold):  # Stop-loss
    #                 data.loc[i, 'Signal'] = -1
    #                 buy_price = None
    #             elif data['Pattern'].iloc[i] == 'Head and Shoulders Top':  # Pattern confirmation
    #                 data.loc[i, 'Signal'] = -1
    #                 buy_price = None
    #
    #     return data
    #
    # # Plot the data
    # def plot_signals(data, stock_symbol):
    #     plt.figure(figsize=(14, 7))
    #     plt.plot(data['Datetime'], data['Close'], label='Close Price', alpha=0.5, color='blue')
    #     plt.scatter(data['Datetime'][data['Signal'] == 1],
    #                 data['Close'][data['Signal'] == 1],
    #                 color='green', label='Buy Signal', marker='^', alpha=1)
    #     plt.scatter(data['Datetime'][data['Signal'] == -1],
    #                 data['Close'][data['Signal'] == -1],
    #                 color='red', label='Sell Signal', marker='v', alpha=1)
    #
    #
    #     graph_path = os.path.join('static', 'TechnicalAnalysisWithBuyAndSellSignals.png')
    #
    #
    #     plt.plot(data['Datetime'], data['BB_Upper'], label='Bollinger Upper', linestyle='--', alpha=0.7, color='orange')
    #     plt.plot(data['Datetime'], data['BB_Lower'], label='Bollinger Lower', linestyle='--', alpha=0.7, color='orange')
    #     plt.scatter(data['Datetime'], data['Support'], color='cyan', label='Support Levels', alpha=0.7)
    #     plt.scatter(data['Datetime'], data['Resistance'], color='magenta', label='Resistance Levels', alpha=0.7)
    #     plt.title(f"{stock_symbol} Advanced Buy/Sell Signals")
    #     plt.xlabel("Datetime")
    #     plt.ylabel("Price")
    #     plt.legend()
    #     plt.grid()
    #     print(f"Graph saved at: {graph_path}")
    #     plt.savefig(graph_path)
    #     plt.close()
    #
    #
    #
    # # Main function
    # def main(stock_symbol):
    #     data = get_stock_data(stock_symbol)
    #     if data is not None:
    #         data = calculate_support_resistance(data)
    #         data = add_indicators(data)
    #         data = detect_patterns(data)
    #         data = generate_signals(data)
    #         plot_signals(data, stock_symbol)
    #
    # # Example usage
    # # if __name__ == "__main__":
    # #     # stock_symbol = 'ebay'  # Example stock
    # #     #
    # #     # main(stock_symbol)
    # #
    #
    #
    # return main(stock_name)

    import numpy as np
    import pandas as pd
    import yfinance as yf
    import matplotlib.pyplot as plt
    import os

    # Fetch historical stock data
    ticker = stock_name  # Change this to your stock symbol
    data = yf.download(ticker, start="2024-06-01", end="2025-02-01")

    # Moving Averages for trend detection
    short_window = 10
    long_window = 50

    # Calculate moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    # Initialize buy & sell signals
    buy_signals = []
    sell_signals = []
    holding = False
    last_buy_price = 0
    max_price_after_buy = 0

    # Convert Close prices to NumPy array for efficiency
    close_prices = data['Close'].values

    for i in range(1, len(data)):
        short_ma_prev, long_ma_prev = data['Short_MA'].iloc[i - 1], data['Long_MA'].iloc[i - 1]
        short_ma_now, long_ma_now = data['Short_MA'].iloc[i], data['Long_MA'].iloc[i]
        current_price = float(close_prices[i])

        # 📌 Advanced Buy Signal
        if (
                not holding
                and short_ma_now > long_ma_now
                and short_ma_prev <= long_ma_prev
                and current_price > np.mean(close_prices[max(0, i - 5):i])
        ):
            buy_signals.append((data.index[i], current_price))
            last_buy_price = current_price
            max_price_after_buy = current_price
            holding = True

            # Update max price after buying
        if holding:
            max_price_after_buy = max(max_price_after_buy, current_price)

        # 📌 Advanced Sell Signal
        if (
                holding
                and max_price_after_buy >= last_buy_price * 1.10
                and current_price < max_price_after_buy * 0.97
        ):
            sell_signals.append((data.index[i], current_price))
            holding = False

            # Extract buy/sell dates & prices
    buy_dates, buy_prices = zip(*buy_signals) if buy_signals else ([], [])
    sell_dates, sell_prices = zip(*sell_signals) if sell_signals else ([], [])

    # Plot the stock closing price
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label="Close Price", color='blue')

    # Plot buy and sell signals
    plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy Signal', s=100, alpha=1)
    plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell Signal', s=100, alpha=1)

    # Formatting
    plt.title(f"{ticker} Stock Trading Signals (Advanced Strategy)")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()

    # **Save the plot to the static folder**
    plot_path = os.path.join("static", "trading_signals.png")
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free memory

    print(f"Plot saved at {plot_path}")





