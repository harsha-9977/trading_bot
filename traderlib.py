# encoding :utf-8

# import alpaca_trade_api as tradepi

import sys, os, time, pytz
import tulipy as ti
import pandas as pd

from datetime import datetime
from math import ceil


class Trader:
    def __init__(self,ticker):
        logging.info("Trader initialized with ticker" % ticker)
        self.ticker = ticker
    def is_tradable(self,ticker):
        # ask the broker/API if "ticker" is tradable
            # IN: ticker (string)
            # OUT: True (tradable) / False (not tradable)
        try :
            # ticker = get ticker from alpaca wrapper (.tradable)
            if not ticker.tradable:
                logging.info("The ticker %s is not tradable" % ticker)
                return False
            else :
                logging.info("The ticker %s is tradable!" % ticker)
                return True
        except :
            logging.info("The ticker %s is not answering well" % ticker)
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
            logging.error("The trend value is not understood: %s" % str(trend))  
            sys.exit() 
    
    def set_takeprofit(self,entryPrice,trend):
        # takes a price as an input and sets the takeprofit 
            # IN: buying/entry price , trend (long/short)  
            # OUT: take profit 

        try:
            if trend == "long":
                # example: 10 + (10*0.1) = 11$
                takeProfit = entryPrice + (entryPrice * gvars.takeProfitMargin)
                logging.info("Take profit set for long at %.2f" % takeprofit)
                return takeProfit
            elif trend == "short":
                # example: 10 - (10*0.05) = 9$
                takeProfit = entryPrice - (entryPrice * gvars.takeProfitMargin)
                logging.info("Take profit set for short at %.2f" % takeprofit)
                return takeProfit
            else:
                raise ValueError
            
        except Exception as e:
            logging.error("The trend value is not understood: %s" % str(trend))  
            sys.exit() 
  
    # load historical stock data:
        # IN: ticker,interval,entries limit
        # OUT: array with stock data (OHLC)

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
         
    # submit order: get our order through the API (look/retry)
        # IN: order data (number of shares, order type)
        # OUT: boolean (True = order went through, False = order did not)

    # cancel order: cancels our order (retry)
        # IN: order ID
        # OUT: boolean (True = order went through, False = order not cancelled)

    def check_position(self,ticker,doNotFind=False):
        # check whether the position exists or not
            # IN: ticker, doNotFind (means that i dont want to find)
            # OUT: boolean (True = order is there, False = order not there)
            attempt = 1

            while attempt <= gvars.maxAttemptCP:
                try:
                    # position = ask the alpaca wrapper for a position
                    currentPrice = position.current_price
                    logging.info("The position was found, Current price is: %.2f" % currentPrice)
                    return True
                except: 

                    if doNotFind:
                        logging.info("Position not found, this is good!")
                        return False

                    logging.info("Position not found, waiting for it...")
                    time.sleep(gvars.sleepTimeCP) # wait 5 seconds and retry
                    attempt += 1

            logging.info("Position not found for %s, not waiting any more" % ticker)      
            return False

    def get_shares_amount(self,tickerPrice):
        # works out the number of shares I want to buy/sell
            # IN: tickerPrice
            # OUT: number of shares
        
        logging.info("Getting shares amount")

        try:
            # get the total equity available
            # totalEquity = ask Alpaca API for availavle equity
              
            # calculate the number of shares 
            sharesQuantity =int(gvars.maxSpentEquity / tickerPrice) 

            logging.info("Total shares to operate with: %d" % sharesQuantity)

            return sharesQuantity
        except Exception as e:
            logging.error("Something happend at get shares amount")
            logging.error(e)
            sys.exit()

    def get_current_price(self,ticker):
        # get the current price of an ticker with a position open
            # IN: ticker
            # OUT: price ($)

        attempt = 1

        while attempt <= gvars.maxAttemptGCP:
            try:
                # position = ask the alpaca wrapper for a position
                currentPrice = position.current_price
                logging.info("The position was checked, Current price is %.2f" % currentPrice)
                return currentPrice
            except:  
                logging.info("Position not found, cannot check price, waiting for it...")
                time.sleep(gvars.sleepTimeGCP) # wait 5 seconds and retry
                attempt += 1

        logging.error("Position not found for %s, not waiting any more" % ticker)      
        return False

    def get_general_trend(self,ticker):
        # get general trend: detect interesting trend (UP / DOWN / FALSE if not trend)
            # IN: ticker
            # OUT: UP / DOWN / NO TREND (strings)
            # ---if NO TREND go back to "ECHO"  

        logging.info("GENERAL TREND ANALYSIS entered")

        attempt = 1
        maxAttempt = 10 # total time = maxAttempt * 10min (as implemented)

        try:
            while True:

                # data = ask alpaca wrapper for 30 min candles

                # calculate the EMAs
                ema9 = ti.ema(data,9)
                ema26 = ti.ema(data,26)
                ema50 = ti.ema(data,50)

                logging.info("%s general trend EMAs = [%.2f,%.2f,%.2f]" % (ticker,ema9,ema26,ema50) )

                # checking EMAs relative position
                if (ema50 > ema26) and (ema26 > ema9):
                    logging.info("Trend detected for %s: long" % ticker)
                    return "long"
                elif (ema50 < ema26) and (ema50 < ema9):
                    logging.info("Trend detected for %s: short" % ticker)
                    return "short"
                elif attempt <= maxAttempt:
                    logging.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(60*10)
                else:
                    logging.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False
                
        except Exception as e:
            logging.error("Something went wrong at get general trend")  
            logging.error(e)
            sys.exit()  

    def get_instant_trend(self,ticker,trend):
        # get instant trend: confirm the trend detected by GT analysis    
            # IN: ticker, trend (long / short)
            # OUT: True (confirmed) / False (not confirmed)
        
        logging.info("INSTANT TREND ANALYSIS entered")

        attempt = 1
        maxAttempt = 10 # total time = maxAttempt * 30sec (as implemented)
    

        try:
            while True:
                # data = ask alpaca wrapper for 5 min candles

                # calculate the EMAs
                ema9 = ti.ema(data,9)
                ema26 = ti.ema(data,26)
                ema50 = ti.ema(data,50)

                logging.info("%s instant trend EMAs = [%.2f,%.2f,%.2f]" % (ticker,ema9,ema26,ema50) )

                if (trend == "long") and (ema9 > ema26) and (ema26 > ema50):
                    logging.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (ema9 < ema26) and (ema26 < ema50):
                    logging.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= maxAttempt:
                    logging.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(30)
                else:
                    logging.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False
        except Exception as e:
            logging.error("Something went wrong at get instant trend")  
            logging.error(e)
            sys.exit()  

    def get_rsi(self,ticker,trend):
        # get rsi: perform RSI analysis 
            # IN: ticker, trend
            # OUT: True (confirmed) / False (not confirmed)

        logging.info("RSI ANALYSIS entered") 

        attempt = 1
        maxAttempt = 10 # total time = maxAttempt * 20sec (as implemented)
    

        try:
            while True:
                # data = ask alpaca wrapper for 5 min candles

                # calculate the RSI
                rsi = ti.rsi(data, 14) # it uses 14-sample window

                logging.info("%s rsi = [%.2f]" % (ticker,rsi) )

                if (trend == "long") and (rsi > 50) and (rsi < 80):
                    logging.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (rsi < 50) and (rsi > 20):
                    logging.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= maxAttempt:
                    logging.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(20)
                else:
                    logging.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False
        except Exception as e:
            logging.error("Something went wrong at rsi analysis")  
            logging.error(e)
            sys.exit()   

    def get_stochastic(self,ticker,trend):
        # get stochastic: perform STOCHASTIC analysis
            # IN: ticker ,trend
            # OUT: True (confirmed) / False (not confirmed)
        
        logging.info("STOCHASTIC ANALYSIS entered") 

        attempt = 1
        maxAttempt = 20 # total time = maxAttempt * 10sec (as implemented)
    

        try:
            while True:
                # data = ask alpaca wrapper for 5 min candles

                # calculate the STOCHASTIC
                stoch_k, stoch_d = ti.stoch(high, low, close, 9, 6, 9)

                logging.info("%s stochastic = [%.2f,%.2f]" % (ticker,stoch_k,stoch_d) )

                if (trend == "long") and (stoch_k > stoch_d) and (stoch_k < 80) and (stoch_d < 80):
                    logging.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (stoch_k < stoch_d) and (stoch_k > 20) and (stoch_d > 20):
                    logging.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= maxAttempt:
                    logging.info("Trend not clear for %s, waiting..." % ticker)
                    attempt += 1
                    time.sleep(10)
                else:
                    logging.info("Trend NOT detected and timeout reached for %s" % ticker)
                    return False
        except Exception as e:
            logging.error("Something went wrong at stochastic analysis")  
            logging.error(e)
            sys.exit()  

    def check_stochastic_crossing(self,ticker,trend):
        # check whether the stochastic curves have crossed or not
        # depending on the trend
            # IN: ticker, trend
            # OUT: True if crossed / False if not crossed
        logging.info("Checking stochasting crossing...")
        # get stochastic values
        # data = ask alpaca wrapper for 5 min candles

        # calculate the STOCHASTIC
        stoch_k, stoch_d = ti.stoch(high, low, close, 9, 6, 9)

        logging.info("%s stochastic = [%.2f,%.2f]" % (ticker,stoch_k,stoch_d) )

        try:
            if (trend == "long") and (stoch_k <= stoch_d):
                logging.info("Stochastic curves crossed: long, k=%.2f, d=%.2f" % (stoch_k,stoch_d))
                return True
            elif (trend == "short") and (stoch_k <= stoch_d):
                logging.info("Stochastic curves crossed: short, k=%.2f, d=%.2f" % (stoch_k,stoch_d))
                return True
            else:
                logging.info("Stochastic curves have not crossed")
                return False
            
        except Exception as e:
            logging.error("Something went wrong at check stochastic crossing")
            logging.error(e)
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

                currentPrice = get_current_price(ticker)
                
                # check if take Profit met
                # LONG/UP version
                if (trend == "long") and (currentPrice >= takeProfit):
                    logging.info("Take profit met at %.2f. Current price is%.2f" % (takeProfit,currentPrice))
                    return True 
                # SHORT/DOWN version
                elif (trend == "short") and (currentPrice <= takeProfit):
                    logging.info("Take profit met at %.2f. Current price is%.2f" % (takeProfit,currentPrice))
                    return True
                
                # check if stop loss is met
                # LONG/UP version
                elif (trend == "long") and (currentPrice <= stopLoss):
                    logging.info("Stop loss met at %.2f. Current price is %.2f" % (stopLoss,currentPrice))
                    return False
                # SHORT/DOWN version
                elif (trend == "short") and (currentPrice <= stopLoss):
                    logging.info("Stop loss met at %.2f. Current price is %.2f" % (stopLoss,currentPrice))
                    return False    

                # check stochastic crossing
                elif check_stochastic_crossing(ticker,trend):
                    logging.info("Stochastic curves crossed. Current price is %.2f" % currentPrice)
                    return True
                
                # we wait
                elif attempt <= maxAttempt:
                    logging.info("Waiting inside position, attempt #&d" % attempt)
                    logging.info("%.2f <-- %.2f --> %.2f" % (stopLoss,currentPrice,takeProfit))
                    time.sleep(20)

                # get out, time is out
                else:
                    logging.info("Timeout reached at enter position, too late")
                    return False
                
        except Exception as e:
            logging.error("Something happend at your position function")
            logging.error(e)
            return True

    def run(self) : 

        # LOOP until timeout reached (ex. 2h)
        while True:
            # POINT "ECHO": INITIAL CHECK --- coming to "ECHO"
            # ask the broker/API if we have an open position with "ticker"
            if check_position(self.ticker,doNotFind=True):
                logging.info("There is already an open position with that ticker! Aborting...")
                return False # aborting execution
            
            # POINT DELTA

            while True:

                # find general trend
                trend = get_general_trend(self.ticker)
                if not trend:
                    logging.info("No general trend found for %s! Going out..." % self.ticker)
                    return False # aborting execution
                
                # confirm instant trend
                if not get_instant_trend(self.ticker,trend):
                    logging.info("The instant trend is not confirmed. Going back")
                    continue # if failed --- go back to POINT "DELTA"
                    
                # perform RSI analysis
                if not get_rsi(self.ticker,trend):
                    logging.info("Then rsi is not confirmed. Going back")
                    continue # if failed --- go back to POINT "DELTA"

                # perform STOCHASTIC analysis
                if not get_stochastic(self.ticker,trend):
                    logging.info("Then stochastic is not confirmed. Going back")
                    continue # if failed --- go back to POINT "DELTA"
                
                logging.info("All filtering passed, carring on with the order!")
                break

            # get current price
            self.currentPrice = get_current_price(self.ticker)

            # decide the total amount to invest
            sharesQuantity = get_shares_amount(self.ticker,self.currentPrice)

            # submit Order (limit)
                # if false, abort / go back to POINT ECHO

            # check the position
            if not check_position(self.ticker):
                # cancel pending order
                continue # go back to POINT ECHO
            
            # enter position mode
            successfullOperation = enter_position_mode(self.ticker,trend)
               

            # GET OUT
            while True:
                # Submit Order (market)

                # check the position is cleared
                if not check_position(self.ticker,doNotfound=True):
                    break
                time.sleep(10) # wait 10 seconds

            # END of execution
            return successfullOperation    
           


