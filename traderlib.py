# encoding :utf-8

# import alpaca_trade_api as tradepi

import sys, os, time, pytz
import tulipy as ti
import pandas as pd
import yfinance as yf
from logger import *
import gvars

from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta
from math import ceil
from enum import Enum

class TimeFrame(Enum):
    Day = "1Day"
    Hour = "1Hour"
    Minute = "1Min"
    Sec = "1Sec"


class Trader:
    def __init__(self,ticker,api):
        lg.info("Trader initialized with ticker %s" % ticker)
        self.ticker = ticker
        self.api = api

    def is_tradable(self,ticker):
        # ask the broker/API if "ticker" is tradable
            # IN: ticker (string)
            # OUT: True (tradable) / False (not tradable)
        try :
            # ticker = get ticker from alpaca wrapper (.tradable)
            if not ticker.tradable:
                lg.info("The ticker %s is not tradable" % ticker)
                return False
            else :
                lg.info("The ticker %s is tradable!" % ticker)
                return True
        except :
            lg.error("The ticker %s is not answering well" % ticker)
            return False

    def set_stoploss(self,entryPrice,trend):
        # takes a price as a input and sets the stoploss
            # IN: buying/entry price,trend (long/short)
            # OUT: stop loss

        try:
            if trend == "long":
                # example: 10 - (10*0.05) = 9.5
                stopLoss = entryPrice - (entryPrice * gvars.stopLossMargin)
                return stopLoss
            elif trend == "short":
                # example: 10 + (10*0.05) = 10.5
                stopLoss = entryPrice + (entryPrice * gvars.stopLossMargin)
                return stopLoss
            else:
                raise ValueError

        except Exception as e:
            lg.error("The trend value is not understood: %s" % str(trend))
            sys.exit()

    def set_takeprofit(self,entryPrice,trend):
        # takes a price as an input and sets the takeprofit
            # IN: buying/entry price , trend (long/short)
            # OUT: take profit

        try:
            if trend == "long":
                # example: 10 + (10*0.1) = 11$
                takeProfit = entryPrice + (entryPrice * gvars.takeProfitMargin)
                lg.info("Take profit set for long at %.2f" % takeprofit)
                return takeProfit
            elif trend == "short":
                # example: 10 - (10*0.05) = 9$
                takeProfit = entryPrice - (entryPrice * gvars.takeProfitMargin)
                lg.info("Take profit set for short at %.2f" % takeprofit)
                return takeProfit
            else:
                raise ValueError

        except Exception as e:
            lg.error("The trend value is not understood: %s" % str(trend))
            sys.exit()

    def load_historical_data(self,ticker,interval,period):
        # load historical stock data:
            # IN: ticker,interval (aggregation),api,entries limit
            # OUT: array with stock data (OHLC)
            data = self.api.get_barset(ticker,interval,limit).df
            import pdb; pdb.set_trace()

        # try:
        #     ticker = yf.Ticker(ticker)
        #     data = ticker.history(interval,period)
        # except Exception as e:
        #     lg.error("Something happened while loaading historical data")
        #     lg.error(e)
        #     sys.exit()
        #
            return data

    def get_open_positions(self,tickerId):
        # get open positions
            # IN: tickerId (unique identifier)
            # OUT: boolean (True = already open, False = not open)

        # postions = ask wrapper for the list of open positions
        for position in positions:
            if position.symbol == tickerId:
                return True
            else:
                return False

    # def submit_order(self,type,trend,ticker,sharesQty,currentPrice,exit=False):
    #     # IN: order data (number of shares, order type)
    #     # OUT: boolean (True = order went through, False = order did not)
    #
    #     lg.info('Submitting %s order for %s' % (trend,ticker))
    #
    #     if trend == 'long' and not exit:
    #         side = 'buy'
    #         limitPrice = round(currentPrice + currentPrice*gvars.maxVar,2)
    #     elif trend == 'short' and not exit:
    #         side = 'sell'
    #         limitPrice = round(currentPrice - currentPrice*gvars.maxVar,2)
    #     elif trend == 'long' and exit:
    #         side = 'sell'
    #     elif trend == 'short' and exit:
    #         side = 'buy'
    #     else:
    #         lg.error('Trend was not understood')
    #         sys.exit()
    #
    #     try:
    #
    #         if type == 'limit':
    #             lg.info('Current price: %.2f // Limit price: %.2f' % (currentPrice,limitPrice))
    #             order = self.api.submit_order(
    #                 symbol=ticker,
    #                 qty=sharesQty,
    #                 side=side,
    #                 type=type,
    #                 time_in_force='gtc',
    #                 limit_price=limitPrice
    #             )
    #
    #         elif type == 'market':
    #             lg.info('Current price: %.2f' % currentPrice)
    #             order = self.api.submit_order(
    #                 symbol=ticker,
    #                 qty=sharesQty,
    #                 side=side,
    #                 type=type,
    #                 time_in_force='gtc'
    #             )
    #
    #         else:
    #             lg.error('Type of order was not undersood')
    #             sys.exit()
    #
    #         self.orderId = order.id
    #
    #         lg.info('%s order submitted correctly!' % trend)
    #         lg.info('%d shares %s for %s' % (sharesQty,side,ticker))
    #         lg.info('Client order ID: %s' % self.orderId)
    #         return True
    #
    #     except Exception as e:
    #         lg.error('Something happend when submitting order')
    #         lg.error(e)
    #         sys.exit()

    # cancel order: cancels our order (retry)
        # IN: order ID
        # OUT: boolean (True = order went through, False = order not cancelled)
        # def cancel_pending_order(self,ticker):
        #     # cancel order: cancels our order (retry)
        #         # IN: order id
        #         # OUT: boolean (True = order cancelled, False = order not cancelled)
        #     lg.info('Cancelling order %s for %s' % (self.orderId,ticker))
        #     attempt = 1
        #
        #     while attempt <= gvars.maxAttemptsCPO:
        #         try:
        #             self.api.cancel_order(self.orderId)
        #             lg.info('Order %s cancelled correctly' % self.orderId)
        #             return True
        #         except:
        #             lg.info('Order could not be cancelled, retrying...')
        #             time.sleep(gvars.sleepTimeCPO) # wait 5 seconds and retry
        #             attempt += 1
        #
        #     lg.error('The order could not be cancelled, cancelling all orders...')
        #     lg.info('Client order ID: %s' % self.orderId)
        #     self.api.cancel_all_orders()
        #     sys.exit()

    def check_position(self,ticker,doNotFind=False):
        # check whether the position exists or not
            # IN: ticker, doNotFind (means that i dont want to find)
            # OUT: boolean (True = order is there, False = order not there)
            attempt = 1

            while attempt <= gvars.maxAttemptCP:
                try:
                    # import pdb; pdb.set_trace()
                    position = self.api.get_position(ticker)
                    self.currentPrice = position.current_price
                    lg.info("The position was found, Current price is: %.2f" % self.currentPrice)
                    return True
                except:
                    if doNotFind:
                        lg.info("Position not found, this is good!")
                        return False

                    lg.info("Position not found, waiting for it...")
                    time.sleep(gvars.sleepTimeCP) # wait 5 seconds and retry
                    attempt += 1

            lg.info("Position not found for %s, not waiting any more" % ticker)
            return False

    def get_shares_amount(self,tickerPrice):
        # works out the number of shares I want to buy/sell
            # IN: tickerPrice
            # OUT: number of shares

        lg.info("Getting shares amount")

        try:
            # get the total equity available
            # totalEquity = ask Alpaca API for availavle equity

            # calculate the number of shares
            sharesQuantity =int(gvars.maxSpentEquity / tickerPrice)

            lg.info("Total shares to operate with: %d" % sharesQuantity)

            return sharesQuantity
        except Exception as e:
            lg.error("Something happend at get shares amount")
            lg.error(e)
            sys.exit()

    def get_current_price(self,ticker):
        # get the current price of an ticker with a position open
            # IN: ticker
            # OUT: price ($)

        attempt = 1

        while attempt <= gvars.maxAttemptGCP:
            try:
                # position = ask the alpaca wrapper for a position
                self.currentPrice = position.current_price
                lg.info("The position was checked, Current price is %.2f" % self.currentPrice)
                return self.currentPrice
            except:
                lg.info("Position not found, cannot check price, waiting for it...")
                time.sleep(gvars.sleepTimeGCP) # wait 5 seconds and retry
                attempt += 1

        lg.error("Position not found for %s, not waiting any more" % ticker)
        return False

    def get_general_trend(self,ticker):
        # get general trend: detect interesting trend (UP / DOWN / FALSE if not trend)
            # IN: ticker
            # OUT: UP / DOWN / NO TREND (strings)
            # ---if NO TREND go back to "ECHO"

        lg.info("GENERAL TREND ANALYSIS entered")

        attempt = 1
        maxAttempt = 10 # total time = maxAttempt * 10min (as implemented)

        try:
            while True:

                # period = 50 samples * 16windows = 5days
                # ask for 30 min candles
                data = self.load_historical_data(ticker,interval="30Min",period="5d")
                close = data.Close.values

                # calculate the EMAs
                ema9 = ti.ema(data.close,9)[-1]
                ema26 = ti.ema(data.close,26)[-1]
                ema50 = ti.ema(data.close,50)[-1]

                lg.info("%s general trend EMAs = [EMA9%.2f,EMA26%.2f,EMA50%.2f]" % (ticker,ema9,ema26,ema50) )

                # checking EMAs relative position
                if (ema50 > ema26) and (ema26 > ema9):
                    lg.info("Trend detected for %s: long" % ticker)
                    return "long"
                elif (ema50 < ema26) and (ema50 < ema9):
                    lg.info("Trend detected for %s: short" % ticker)
                    return "short"
                elif attempt <= maxAttempt:
                    lg.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(60*10)
                else:
                    lg.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False

        except Exception as e:
            lg.error("Something went wrong at get general trend")
            lg.error(e)
            sys.exit()

    def get_instant_trend(self,ticker,trend):
        # get instant trend: confirm the trend detected by GT analysis
            # IN: ticker, trend (long / short)
            # OUT: True (confirmed) / False (not confirmed)

        lg.info("INSTANT TREND ANALYSIS entered")

        attempt = 1
        maxAttempt = 10 # total time = maxAttempt * 30sec (as implemented)


        try:
            while True:
                #period = 50 samples of 5 minutes =  1days
                data = self.load_historical_data(ticker,interval="5m",period="1d")
                close = data.Close.values

                # calculate the EMAs
                ema9 = ti.ema(data.close,9)[-1]
                ema26 = ti.ema(data.close,26)[-1]
                ema50 = ti.ema(data.close,50)[-1]

                lg.info("%s instant trend EMAs = [%.2f,%.2f,%.2f]" % (ticker,ema9,ema26,ema50) )

                if (trend == "long") and (ema9 > ema26) and (ema26 > ema50):
                    lg.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (ema9 < ema26) and (ema26 < ema50):
                    lg.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= maxAttempt:
                    lg.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(30)
                else:
                    lg.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False
        except Exception as e:
            lg.error("Something went wrong at get instant trend")
            lg.error(e)
            sys.exit()

    def get_rsi(self,ticker,trend):
        # get rsi: perform RSI analysis
            # IN: ticker, trend
            # OUT: True (confirmed) / False (not confirmed)

        lg.info("RSI ANALYSIS entered")

        attempt = 1
        maxAttempt = 10 # total time = maxAttempt * 20sec (as implemented)


        try:
            while True:
                # period  = 50 samples of 5 minutes = 1days
                data = self.load_historical_data(ticker,interval="5m",limit="1d")

                # calculate the RSI
                rsi = ti.rsi(data.Close.values, 14)[-1] # it uses 14-sample window

                lg.info("%s rsi = [%.2f]" % (ticker,rsi) )

                if (trend == "long") and (rsi > 50) and (rsi < 80):
                    lg.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (rsi < 50) and (rsi > 20):
                    lg.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= maxAttempt:
                    lg.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(20)
                else:
                    lg.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False
        except Exception as e:
            lg.error("Something went wrong at rsi analysis")
            lg.error(e)
            sys.exit()

    def get_stochastic(self,ticker,trend):
        # get stochastic: perform STOCHASTIC analysis
            # IN: ticker ,trend
            # OUT: True (confirmed) / False (not confirmed)

        lg.info("STOCHASTIC ANALYSIS entered")

        attempt = 1
        maxAttempt = 20 # total time = maxAttempt * 10sec (as implemented)


        try:
            while True:
                # period  = 50 samples of 5 minutes = 1days
                data = self.load_historical_data(ticker,interval="5m",limit="1d")

                # calculate the STOCHASTIC
                stoch_k, stoch_d = ti.stoch(data.High.values,data.Low.values,data.Close.values, 9, 6, 9)
                stoch_k = stoch_k[-1]
                stock_d = stoch_d[-1]

                lg.info("%s stochastic = [%.2f,%.2f]" % (ticker,stoch_k,stoch_d) )

                if (trend == "long") and (stoch_k > stoch_d) and (stoch_k < 80) and (stoch_d < 80):
                    lg.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (stoch_k < stoch_d) and (stoch_k > 20) and (stoch_d > 20):
                    lg.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= gvars.maxAttemptSTC:
                    lg.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(gvars.maxAttemptSTC)
                else:
                    lg.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False
        except Exception as e:
            lg.error("Something went wrong at stochastic analysis")
            lg.error(e)
            sys.exit()

    def check_stochastic_crossing(self,ticker,trend):
        # check whether the stochastic curves have crossed or not
        # depending on the trend
            # IN: ticker, trend
            # OUT: True if crossed / False if not crossed
        lg.info("Checking stochasting crossing...")
        # get stochastic values
        # period  = 50 samples of 5 minutes = 1days
        data = self.load_historical_data(ticker,interval="5m",limit="1d")

        # calculate the STOCHASTIC
        stoch_k, stoch_d = ti.stoch(data.High.values,data.Low.values,data.Close.values, 9, 6, 9)
        stoch_k = stoch_k[-1]
        stock_d = stoch_d[-1]

        lg.info("%s stochastic = [%.2f,%.2f]" % (ticker,stoch_k,stoch_d) )

        try:
            if (trend == "long") and (stoch_k <= stoch_d):
                lg.info("Stochastic curves crossed: long, k=%.2f, d=%.2f" % (stoch_k,stoch_d))
                return True
            elif (trend == "short") and (stoch_k <= stoch_d):
                lg.info("Stochastic curves crossed: short, k=%.2f, d=%.2f" % (stoch_k,stoch_d))
                return True
            else:
                lg.info("Stochastic curves have not crossed")
                return False

        except Exception as e:
            lg.error("Something went wrong at check stochastic crossing")
            lg.error(e)
            return True

    def enter_position_mode(self,ticker,trend):
        # check the condition in PARALLEL once inside the position (LOOP_2) ---if not go to 1

        attempt = 1
        maxAttempt = 1260 # calculate 7h total: 7*60*60 / 20

        # entryPrice = ask the alpaca API for the entry price

        # set the take profit
        takeProfit = set_takeprofit(entryPrice,trend)

        # set the stop loss
        stopLoss = set_stoploss(entryPrice,trend)
        try:
            while True:

                self.currentPrice = self.get_current_price(ticker)

                # check if take Profit met
                # LONG/UP version
                if (trend == "long") and (self.currentPrice >= takeProfit):
                    lg.info("Take profit met at %.2f. Current price is%.2f" % (takeProfit,self.currentPrice))
                    return True
                # SHORT/DOWN version
                elif (trend == "short") and (self.currentPrice <= takeProfit):
                    lg.info("Take profit met at %.2f. Current price is%.2f" % (takeProfit,self.currentPrice))
                    return True

                # check if stop loss is met
                # LONG/UP version
                elif (trend == "long") and (self.currentPrice <= stopLoss):
                    lg.info("Stop loss met at %.2f. Current price is %.2f" % (stopLoss,self.currentPrice))
                    return False
                # SHORT/DOWN version
                elif (trend == "short") and (self.currentPrice <= stopLoss):
                    lg.info("Stop loss met at %.2f. Current price is %.2f" % (stopLoss,self.currentPrice))
                    return False

                # check stochastic crossing
                elif check_stochastic_crossing(ticker,trend):
                    lg.info("Stochastic curves crossed. Current price is %.2f" % self.currentPrice)
                    return True

                # we wait
                elif attempt <= maxAttempt:
                    lg.info("Waiting inside position, attempt #&d" % attempt)
                    lg.info("%.2f <-- %.2f --> %.2f" % (stopLoss,self.currentPrice,takeProfit))
                    time.sleep(20)

                # get out, time is out
                else:
                    lg.info("Timeout reached at enter position, too late")
                    return False

        except Exception as e:
            lg.error("Something happend at your position function")
            lg.error(e)
            return True

    def run(self,ticker) :

        # LOOP until timeout reached (ex. 2h)
        while True:
            # POINT "ECHO": INITIAL CHECK --- coming to "ECHO"
            # ask the broker/API if we have an open position with "ticker"
            if self.check_position(self.ticker,doNotFind=True):
                lg.info("There is already an open position with that ticker! Aborting...")
                return False # aborting execution

            # POINT DELTA

            while True:

                # find general trend
                trend = self.get_general_trend(self.ticker)
                if not trend:
                    lg.info("No general trend found for %s! Going out..." % self.ticker)
                    return False # aborting execution

                # confirm instant trend
                if not self.get_instant_trend(self.ticker,trend):
                    lg.info("The instant trend is not confirmed. Going back")
                    continue # if failed --- go back to POINT "DELTA"

                # perform RSI analysis
                if not self.get_rsi(self.ticker,trend):
                    lg.info("Then rsi is not confirmed. Going back")
                    continue # if failed --- go back to POINT "DELTA"

                # perform STOCHASTIC analysis
                if not self.get_stochastic(self.ticker,trend):
                    lg.info("Then stochastic is not confirmed. Going back")
                    continue # if failed --- go back to POINT "DELTA"

                lg.info("All filtering passed, carring on with the order!")
                break

            # get current price
            self.currentPrice = float(self.load_historical_data(ticker,interval="1min",period="1d").Close.values[-1],2)

            # decide the total amount to invest
            sharesQty = self.get_shares_amount(self.currentPrice)

            lg.info("\nDESIRED ENTRY PRICE: %.2f" % self.currentPrice)
            # submit Order (limit)
                # if false, abort / go back to POINT ECHO
            success = self.submit_order(
                            "limit",
                            trend,
                            ticker,
                            sharesQty,
                            self.currentPrice
                            )
            # check the position
            if not self.check_position(self.ticker):
                # cancel pending order
                continue # go back to POINT ECHO

            # enter position mode
            successfullOperation = self.enter_position_mode(self.ticker,trend)


            # GET OUT
            while True:
                # Submit Order (market)

                # check the position is cleared
                if not self.check_position(self.ticker,doNotfound=True):
                    break
                time.sleep(10) # wait 10 seconds

            # END of execution
            return successfullOperation
