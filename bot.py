# encoding: utf-8

# import needed libraries
#from traderlib import *
from logger import *
import sys

import alpaca_trade_api as tradeapi

import gvars

# check our trading account (blocked? total amount?)
def check_account_ok() :
    try :
        print("Checking")
    except Exception as e :
        logging.error("Could not get account info")
        logging.info(str(e))
        sys.exit()

# close current orders (doublecheck)
def clean_open_orders() :
    # open orders = list of open orders
    logging.info("List of open orders")
    logging.info(str(open_orders))

    for order in open_orders :
        # close order
        logging.info("order %s closed "% str(order.id))

    logging.info("Closing orders complete")

# execute trading bot
def main() :

    api = tradeapi.REST(gvars.API_KEY, gvars.API_SECRET_KEY, gvars.API_URL, '<key_id>', '<secret_key>', api_version="v2")
    import pdb; pdb.set_trace()

    # OUT: boolean tradingSuccess  (True = success / False = failure)

    # initialize the logger (imported from logger)
    initialize_logger()

    # check our trading account
    check_account_ok()

    # close current orders
    clean_open_orders()

    # get ticker
    ticker = input("Write the ticker you want to operate with: ")

    trader = Trader(ticker) # initialize trading bot
    trader.run() # run trading bot library

    if not tradingSuccess:
        logging.info("Trading was not successful, locking asset")
        # wait whatever time

if __name__ == '__main__' :
    main()
