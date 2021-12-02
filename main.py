import re
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


def login():
    """Login to account"""


    print("************************")
    print("         LOGIN          ")
    print("************************")

    username = input('Enter username: ')
    password = input('Enter password: ')

    # create
    user_loaded = stockgame.load_user(username, password)

    if user_loaded:
        mainMenu()

    else:
        startMenu()


def register():
    """Create new user"""

    print("************************")
    print("        REGISTER        ")
    print("************************")
    username = input('Enter username: ')
    password = input('Enter password: ')

    # create
    user_created = stockgame.create_user(username, password)

    if not user_created:
        register()
    else:
        return user_created


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


def mainMenu():

    user = stockgame.name

    mainMenuText = f"""
************************************
*            MAIN MENU             *
************************************
* Welcome {user}                   *
* Please select an option          *
* 1. View portfolio                *
* 2. Buy                           *
* 3. Sell                          *
* 4. Search stock                  *
* 5. Logout                        *
************************************"""

    choice = valMenu(mainMenuText, ["1", "2", "3", "4"])
    if choice == "1":
        pass
        #view_portfolio()
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


if __name__ == '__main__':
    stockgame = StockGame()
    startMenu()
