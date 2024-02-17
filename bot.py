# encoding: utf-8

# import needed libraries
# from traderlib import *
from logger import *
# from loggi import *
# initialize_logger()
# initialize_logger()

import sys

import alpaca_trade_api as tradeapi

import gvars

# check our trading account (blocked? total amount?)
def check_account_ok(api) :
    try :
        account = api.get_account()
        if account.status != 'ACTIVE':
            lg.error("The account is not ACTIVE, aborting")
            sys.exit()
    except Exception as e :
        lg.error("Could not get account info")
        lg.info(str(e))
        sys.exit()

# close current orders (doublecheck)
def clean_open_orders() :
    open orders = list of open orders
    lg.info("List of open orders")
    lg.info(str(open_orders))

    for order in open_orders :
        # close order
        lg.info("order %s closed " % str(order.id))

    lg.info("Closing orders complete")

# execute trading bot
def main() :

    api = tradeapi.REST(gvars.API_KEY, gvars.API_SECRET_KEY, gvars.API_URL)

    # OUT: boolean tradingSuccess  (True = success / False = failure)

    # initialize the logger (imported from logger)
    initialize_logger()

    # check our trading account
    check_account_ok(api)

    # close current orders
    clean_open_orders()

    # get ticker
    ticker = input("Write the ticker you want to operate with: ")

    trader = Trader(ticker) # initialize trading bot
    trader.run() # run trading bot library

    if not tradingSuccess:
        lg.info("Trading was not successful, locking asset")
        # wait whatever time

if __name__ == '__main__' :
    main()
