import re
import time
import hashlib
from stockgame import StockGame


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
    elif choice == 4:
        quit()
    return startMenu()


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

    # create
    user_created = stockgame.create_user(username, password)

    if user_created:
        return
    else:
        register()


def mainMenu():

    user = stockgame.name

    mainMenuText = f"""
************************************
*            MAIN MENU             *
************************************
*          Welcome {user}          *
* Please select an option          *
* 1. View portfolio                *
* 2. Buy                           *
* 3. Sell                          *
* 4. Search stock                  *
* 5. Logout                        *
************************************"""

    choice = valMenu(mainMenuText, ["1", "2", "3", "4"])
    if choice == "1":
        view_portfolio()

    elif choice == "2":
        pass
        #buy_stock()
    elif choice == "3":
        pass
        #sell_stock()
    elif choice == 4:
        pass
        #search_stock
    elif choice == 5:
        startMenu()
    return startMenu()


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


if __name__ == '__main__':
    stockgame = StockGame()
    startMenu()
