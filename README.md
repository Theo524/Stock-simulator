# Stock-simulator
This is a text based simple stock simulator which I implemented into my investing basics app for the simulator part(currently private). I made this one here to make a text based one and also extend it further. It works on the json file 'trading.json'.

### Requirements
- python 3

To install the other requirement run the follwing command:
```
pip list --format=freeze > requirements.txt
```

### Demo
main.py is a text based implementation of the stockgame class. It implements all the futures that the class contains. It allows you to create or load users, buying and selling stock as well as researching stocks.

# Stockgame class
The class allows handles all stock related procceses as well as the database file 'trading.json'. Each username is unique.

Create an instance
```python
>>> stock_simulator = StockGame()
```

The first thing you need to do before anything is loading an existing user
```python
>>> stock_simulator.load_user(name='test', password='password')

# Turn true on admin pass if you don't want to enter password
>>> stock_simulator.load_user(name='test', admin_pass=True)

# You can get the following attributes
>>> print(stock_simulator.name)
'test'

>>> print(stock_simulator.current_user) # sample of existing user
{'user_id': 1, 
 'data': 
        {'user_name': 'test', 
         'password': '372a53b95f46e775b973031e40b844f24389657019f7b7540a9f0496f4ead4a2e4b050909664611fb0f4b7c7e92c3c04c84787be7f6b8edf7bf6bc31856b6c76',
         'account_value': 0,
         'cash': 91095.91, 
         'portfolio': [
                  {'AMZN': {'initial_purchase_price': 3426.27, 'quantity': 2, 'total_value': 6854.74}}, 
                  {'EBAY': {'initial_purchase_price': 66, 'quantity': 7, 'total_value': 462.48999999999995}}, 
                  {'FB': {'initial_purchase_price': 317.91, 'quantity': 5, 'total_value': 1589.35}}]}}
              ]
         }
}
```

## Adding and deleting users
You can also create and delete a user
```python

# create user
>>> stock_simulator.create_user(name='user', password='password)
'Created user: user'

# Load and see the new user
>>> stock_simulator.load_user(name='user', password='password')

>>> print(stock_simulator.current_user)
{'user_id': 2, 
 'data': 
        {'user_name': 'user', 
         'password': '3295d7310bd5009601ee9a12eff0a70115058d4c2c24310ccd99a049b3af78a49b320c8681b076873a47c84074151c7111af0ffd1fff7ae32056ff13b83c6636',
         'account_value': 0,
         'cash': 100000, 
         'portfolio': []
        }
}

# delete user
>>> stock_simulator.delete_user(name='user')
'Deleted user: user'

# try loading deleted user
>>> stock_simulator.load_user(name='user')
'User does not exist'

>>> print(stock_simulator.current_user)
None
```

## Buying and selling
Finally, you can buy and sell stocks for a loaded user:
```python
# buying
>>> stock_simulator.buy(ticker='AMZN', quantity=7)
"""---------RECEIPT----------
Stock: AMZN
Quantity: 7
1 share worth: £3490
Total cost: £24430
--------PURCHASE---------
Cash available: £100000
Cash after purchase: £75570
---------------------------"""

>>> stock_simulator.get_portfolio()
[{'AMZN': {'initial_purchase_price': 3490, 'quantity': 7, 'total_value': 23991.59}}]

# selling
>>> stock_simulator.sell(ticker='AMZN', quantity=3)
>>> print(stock.simulator.get_cash())
86039.67

>>> print(stock_simulator.get_portfolio())
[]
```
