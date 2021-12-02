import json
import yfinance as yf
import hashlib
import re


class StockGame:
    def __init__(self):
        """
        current user dict format
        {
            "user_id": ?,
            "data": {
                "user_name": "?",
                "password": "?"
                "account_value": ?,
                "cash": ?,
                "portfolio": [
                    {
                        "?": {
                            "purchase_price": ?,
                            "quantity": ?,
                            "total_value": ?
                        }
                    }
                ]
            }
        }
        """

        self.name = None
        self.current_user = None

    @staticmethod
    def reset_id_numbers():
        """Reset id numbers in json file"""

        # Writing to trading.json
        with open("trading.json", "r+") as file:
            # load file
            file_data = json.load(file)
            # reset user_ids
            id_count = 1
            for val in file_data['users']:
                val['user_id'] = id_count  # set new id
                # increment id count
                id_count += 1

            # move to file_data to json file
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def create_user(self, name, password):
        """Create new user"""

        # if the user exists, exit function
        if self.user_exists(name):
            print('Username already exists')
            return False

        # test password
        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            # match
            password = self.hash_pass(password)
        else:
            # no match
            print("""Invalid password. It must have:
- At least 8 characters
- Must be restricted to, though does not specifically require any of:
    - uppercase letters: A-Z
    - lowercase letters: a-z
    - numbers: 0-9
    - any of the special characters: @#$%^&+=\n
""")
            return False

        # Writing to trading.json
        with open("trading.json", "r+") as file:
            # load file
            file_data = json.load(file)

            # determine id for new user through file length
            user_id = len(file_data['users']) + 1

            # dict of user
            user_info = {

                "user_id": user_id, "data": {"user_name": name, 'password': password, "account_value": 0,
                                             "cash": 100000, "portfolio": []}
            }

            # add new user to json file users
            file_data["users"].append(user_info)

            # move to file_data to json file
            file.seek(0)
            json.dump(file_data, file, indent=4)
            print(f'Created user: "{name}"')
            return True

    def delete_user(self, name):
        """Delete user from json file"""

        # if the user does not exist, exit function
        if not self.user_exists(name):
            return

        # Writing to trading.json
        with open("trading.json", "r+") as file:
            # load file
            file_data = json.load(file)

            # locate user id
            for val in file_data['users']:
                if name == val['data']['user_name']:
                    # if the id is found, break loop
                    user_id = val['user_id']
                    break

            # rebuild dict
            new_data = {"users": [data for data in file_data['users'] if data['user_id'] != user_id]}

        # move new_data to new json file
        with open("trading.json", "w") as file:
            json.dump(new_data, file, indent=4)

        # reset/match ids
        self.reset_id_numbers()

    def load_user(self, name, password='', admin_pass=False):
        """Load user from json file to game"""

        # if user does not exist, exit function
        if not self.user_exists(name):
            return

        # open json
        with open("trading.json", 'r+') as file:
            file_data = json.load(file)

            # Loop trough all the users
            for val in file_data['users']:
                # Find the matching name and password
                if admin_pass:
                    if val['data']['user_name'] == name:
                        self.name = name
                        # if the name matches, set StockGame current user to val
                        self.current_user = val
                        return True

                # without admin pass search for password
                if not admin_pass:
                    if val['data']['user_name'] == name and val['data']['password'] == self.hash_pass(password):
                        self.name = name
                        # if the name matches, set StockGame current user to val
                        self.current_user = val
                        return True

        # no match
        print('Invalid credentials')
        return False

    def buy(self, ticker, quantity):
        """Purchase a stock"""

        # check user has been loaded
        if self.current_user is None:
            return

        # user financial data
        cash = self.current_user["data"]["cash"]
        account_value = self.current_user["data"]["account_value"]

        # yfinance stock object
        ticker_obj = yf.Ticker(ticker).info

        # ticker name
        ticker_name = ticker_obj['symbol']
        # current real time price of ticker
        value = ticker_obj['regularMarketPrice']
        total_value = value * quantity

        # purchase/transaction cost
        price = ticker_obj['bid']
        total_cost_of_buy = price * quantity

        # check if user has the stock
        exists, index = self.user_has_stock(ticker.upper())

        # if the stock does not exist in the user portfolio
        # it is a first time purchase
        if not exists:

            # ticker data to add to portfolio
            holding = {ticker_name: {"initial_purchase_price": price, "quantity": quantity, "total_value": total_value}}

            # open json
            with open("trading.json", "r+") as file:
                # load file
                file_data = json.load(file)

                # add user info to list
                for val in file_data['users']:
                    # find the matching user
                    if val["data"]["user_name"] == self.current_user["data"]["user_name"]:
                        # add stock data(holding) to portfolio
                        val["data"]["portfolio"].append(holding)

                        # update cash available
                        cash_left = val["data"]["cash"] - total_cost_of_buy
                        val["data"]["cash"] = cash_left

                        print("---------RECEIPT----------")
                        print(f"Stock: {ticker_name}")
                        print(f"Quantity: {quantity}")
                        print(f"1 share worth: £{price}")
                        print(f"Total cost: £{price * quantity}")
                        print(f"--------PURCHASE---------")
                        print(f"Cash available: £{cash}")
                        print(f"Cash after purchase: £{cash_left}")
                        print("---------------------------")
                        print('\n\n')

                # move to json file
                file.seek(0)
                json.dump(file_data, file, indent=4)

        # if the stock does exist in the user portfolio
        # just need to update the values
        if exists:

            # open json
            with open("trading.json", "r+") as file:
                # load file
                file_data = json.load(file)

                # find user
                for val in file_data['users']:
                    if val["data"]["user_name"] == self.current_user["data"]["user_name"]:
                        # replace user quantity for the stock with new quantity
                        val["data"]["portfolio"][index][ticker_name]["quantity"] = \
                            self.current_user["data"]["portfolio"][index][ticker_name]["quantity"] + quantity

                        # replace user total value for the stock with new total value
                        val["data"]["portfolio"][index][ticker_name]["total_value"] = \
                            self.current_user["data"]["portfolio"][index][ticker_name]["total_value"] + total_value

                        # cash left available
                        cash_left = val["data"]["cash"] - total_cost_of_buy
                        val["data"]["cash"] = cash_left

                file.seek(0)

                # move to json file
                json.dump(file_data, file, indent=4)

        # after each purchase the current user data must also be updated
        self.load_user(self.name, admin_pass=True)

    def sell(self, ticker, quantity):
        """Sell a stock"""

        # check user has been loaded
        if self.current_user is None:
            return

        # flag to determine whether the stock is to be deleted
        delete_stock = False

        # user financial data
        cash = self.current_user["data"]["cash"]
        account_value = self.current_user["data"]["account_value"]

        # yfinance stock object
        ticker_obj = yf.Ticker(ticker).info

        # ticker name
        ticker_name = ticker_obj['symbol']
        # current real time price of ticker
        value = ticker_obj['regularMarketPrice']
        total_value = value * quantity

        # sell cost
        ask_price = ticker_obj['ask']
        total_cost_of_sell = ask_price * quantity

        # check if user has the stock
        exists, index = self.user_has_stock(ticker)

        if exists:
            # open json
            with open("trading.json", "r+") as file:
                # load file
                file_data = json.load(file)

                # add user info to list
                for val in file_data['users']:
                    # find the matching user
                    if val["data"]["user_name"] == self.current_user["data"]["user_name"]:
                        # add stock data(holding) to portfolio
                        for my_stock in val['data']['portfolio']:
                            # get name for current stock in list
                            stock_symbol = list(my_stock.keys())[0]
                            if stock_symbol == ticker_name:
                                # original quantity
                                original_quantity = self.current_user['data']['portfolio'][index][ticker_name][
                                    'quantity']

                                # new quantity
                                new_quantity = original_quantity - quantity
                                val['data']['portfolio'][index][ticker_name]['quantity'] = new_quantity

                                # total value
                                total_value = new_quantity * value
                                val['data']['portfolio'][index][ticker_name]['total_value'] = total_value

                                # profit
                                val['data']['cash'] = cash + total_cost_of_sell
                                print('HI')

                                if new_quantity <= 0:
                                    # delete the stock if the value is all lost
                                    delete_stock = True
                                    # rebuild dict
                                    new_data = [data for data in val['data']['portfolio'] if list(data.keys())[0] != ticker_name]

                                    # clear user portfolio
                                    val['data']['portfolio'].clear()

                                    # add all stocks except deleted one
                                    for data in new_data:
                                        val['data']['portfolio'].append(data)

                                    # assign this version to a new variable
                                    deleted_stock_file = file_data

            # rewrite data to new file
            with open('trading.json', 'w') as file:
                if delete_stock:
                    json.dump(deleted_stock_file, file, indent=4)

                elif not delete_stock:
                    json.dump(file_data, file, indent=4)

        if not exists:
            print('The user does not have the stock')

        # after each sell the current user data must also be updated
        self.load_user(self.name, admin_pass=True)

    @staticmethod
    def user_exists(name):
        """Confirm if a user exists in the json"""

        # Writing to trading.json
        with open("trading.json", "r+") as file:
            # load file
            file_data = json.load(file)

            for val in file_data['users']:
                # find matching name
                if val['data']['user_name'] == name:
                    print('User exists')
                    return True
        return False

    def user_has_stock(self, ticker):
        """Confirm user owns stock

        return bool and index of item in portfolio
        """

        # obj
        ticker_obj = yf.Ticker(ticker).info

        # index
        index = 0
        # loop through the entire portfolio until a match is found
        for stock in self.current_user["data"]["portfolio"]:
            try:
                # name of current stock
                name = list(stock.keys())[0]
                # if exists return true and index
                if name == ticker:
                    return [True, index]
            except KeyError:
                continue

            # index for next item in portfolio list
            index += 1
        return [False, None]

    def get_portfolio(self):
        """Return portfolio"""

        # check user has been loaded
        if self.current_user is None:
            return

        return self.current_user['data']['portfolio']

    @staticmethod
    def hash_pass(password):
        """Hash the password for better security"""

        # password hashing
        message = password.encode()
        hashed_password = hashlib.blake2b(message).hexdigest()

        # Return result
        return hashed_password
