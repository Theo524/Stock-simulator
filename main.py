import re
import matplotlib.pyplot as plt
import yfinance as yf
import time
import hashlib
from stockgame import StockGame, News


# functionalities
def valMenu(message, options):
    choice = input(message + "\nchoice: ")
    while choice not in options:
        print("you must select from the following options: ", ",".join(options))
        choice = input(message + "\nchoice: ")
    return choice


def hash_pass(password):
    """Hash the password for better security"""

    # password hashing
    message = password.encode()
    hashed_password = hashlib.blake2b(message).hexdigest()

    # Return result
    return hashed_password


# menus
def startMenu():
    startMenuText = """
************************************
*              MENU                *
************************************
* Welcome to the Stock simulator   *
* Please select an option          *
* 1. Login                         *
* 2. Create  user                  *
* 3. Help                          *
* 4. Quit                          *
************************************"""

    choice = valMenu(startMenuText, ["1", "2", "3", "4"])
    if choice == "1":
        login()

    elif choice == "2":
        register()

    elif choice == "3":
        pass
        #showStartMenuHelp()
    elif choice == "4":
        quit()
    return startMenu()


def mainMenu():

    user = stockgame.name

    mainMenuText = f"""
************************************
*            MAIN MENU             *
************************************
*          Welcome {user}          *
*       Please select an option    *
* 1. View portfolio                *
* 2. Buy                           *
* 3. Sell                          *
* 4. Search stock                  *
* 5. Logout                        *
************************************"""

    choice = valMenu(mainMenuText, ["1", "2", "3", "4", "5"])
    if choice == "1":
        view_portfolio()

    elif choice == "2":
        pass
        #buy_stock()
    elif choice == "3":
        pass
        #sell_stock()
    elif choice == "4":
        search_stock()
    elif choice == "5":
        startMenu()
    return mainMenu()


def search_stock():
    """Research a stock"""

    print("************************")
    print("     SEARCH STOCK       ")
    print("************************")

    stock = input('Enter the stock here: ').upper()

    ticker_obj = yf.Ticker(stock).info
    s_type = ticker_obj['quoteType']

    if s_type == 'EQUITY':
        tickerMenu(stock)

    else:
        print('You must enter equities')
        return


def tickerMenu(ticker):
    ticker = ticker
    ticker_obj = yf.Ticker(ticker).info

    tickerMenuText = f"""
************************************
*           {ticker.upper()}         *
************************************
*       Please select an option    *
* 1. Basic statistics              *
* 2. Extended statistics           *
* 3. Line chart                    *
* 4. News                          *
* 5. Exit                          *
************************************"""

    choice = valMenu(tickerMenuText, ["1", "2", "3", "4", "5"])
    if choice == "1":
        # basic data
        price = ticker_obj['regularMarketPrice']
        d_low = ticker_obj['dayLow']
        d_high = ticker_obj['dayHigh']
        prev_close = ticker_obj['previousClose']
        vol = ticker_obj['volume']
        market_cap = ticker_obj['marketCap']
        currency = ticker_obj['currency']

        print('***********************************************************')
        print('Here is the basic data:')
        print(f'price: {price}\nMarket capitalization: {market_cap}\nVolume: {vol}\n'
              f'Previous close: {prev_close}\nDay high: {d_high}\nDay Low: {d_low}\nCurrency: {currency}')
        print('***********************************************************')

    elif choice == "2":
        print('***********************************************************')
        print('Here is the extended data:')
        for k, v in ticker_obj.items():
            print(f'{k}: {v}')
        print('***********************************************************')

    elif choice == "3":
        show_line_chart(ticker)
    elif choice == "4":
        show_news(ticker)
    elif choice == "5":
        return

    return tickerMenu(ticker)


# Pages
def login():
    """Login to account"""


    print("************************")
    print("         LOGIN          ")
    print("************************")

    username = input('Enter username: ')
    password = input('Enter password: ')

    # create load user
    user_loaded = stockgame.load_user(username, password)
    print(user_loaded)

    if user_loaded:
        mainMenu()

    else:
        print('User does not exist')
        return


def register():
    """Create new user"""

    print("************************")
    print("        REGISTER        ")
    print("************************")
    attempts = 0

    while True:
        username = input('Enter username: ')
        password = input('Enter password: ')
        confirm_password = input('Confirm password')
        if confirm_password == password:
            break

        if attempts == 3:
            return

        attempts += 1

    # create user
    user_created = stockgame.create_user(username, password)

    if user_created:
        return
    else:
        register()


def view_portfolio():
    portfolio = stockgame.get_portfolio()
    cash = stockgame.get_cash()
    owned = len(portfolio)

    if owned == 0:
        print('You have got no stocks')
        return

    print("************************")
    print("       PORTFOLIO        ")
    print("************************")
    print(f'Stocks owned: {owned}')
    print(f'Cash available: £{cash}\n')
    print('Your stock(s):')
    c = 1
    for stock in portfolio:
        the_stock = list(stock.items())[0]
        name = the_stock[0]
        data = the_stock[1]

        print(c, name)
        print(f'{data}\n')

        c += 1
    # Give the user time to see portfolio
    time.sleep(3)


def show_news(ticker):

    print("************************")
    print("          NEWS          ")
    print("************************")
    print("Now you will be shown extracts from the 5 most recent article/resources related to this stock:\n")

    n = News(ticker)
    d = n.news_data_dict
    for key, val in d.items():
        print(f'Article number {key + 1}')
        print(val['title'])
        print(f"Extract:\n{val['description']}")
        print(f" {val['date']} • {val['media_src']}")
        print(f"Link: {val['link']}\n")
        time.sleep(4)


def show_line_chart(ticker):

    # ticker obj
    t_name = ticker
    ticker_obj = yf.Ticker(t_name)
    full_name = ticker_obj.info['longName']
    data = None

    chartMenuText = f"""
************************************
*           {full_name}            *
************************************
*    Please select Period range    *
* 1. Day                           *
* 2. Week                          *
* 3. Month                         *
* 4. Year                          *
* 5. max                           *
* 6. Go back                       *
************************************
"""

    choice = valMenu(chartMenuText, ["1", "2", "3", "4", "5", "6"])

    if choice == '1':
        # 1 day data for the stock at 5 minute intervals
        data = ticker_obj.history(period='1d', interval='5m')

    elif choice == '2':
        # 1 week data for the stock at 15 minute interval
        data = ticker_obj.history(period='5d', interval='1d')

    elif choice == '3':
        # 1 month data for the stock at a daily interval
        month_num = valMenu('How many months?[1, 3, 6]: ', ["1", "3", "6"])
        data = ticker_obj.history(period=f'{month_num}mo', interval='1d')

    elif choice == '4':
        # 1 month data for the stock at a daily interval
        year_num = valMenu('How many years?[1, 2, 5, 10]: ', ["1", "2", "5", "10"])
        data = ticker_obj.history(period=f'{year_num}y', interval='1m')

    elif choice == '5':
        # 5 year data for the stock at a weekly interval
        data = ticker_obj.history(period='max', interval='1mo')

    elif choice == "6":
        return

    # plot data
    if data is not None:
        plt.figure()
        plt.plot(data['Close'])
        plt.xlabel('Date')
        plt.legend(['Price ($)'])
        plt.show()

    return show_line_chart(t_name)


if __name__ == '__main__':
    stockgame = StockGame()
    startMenu()
