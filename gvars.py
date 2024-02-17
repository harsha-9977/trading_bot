# encoding: utf-8

# REST API
API_KEY = "PKU3JHWNZWUZA9RBJDDB"
API_SECRET_KEY = "0DmfOX2ShSQX14FmGNxgc1R5nQC0ub1jiJta5mM0"
API_URL = "https://paper-api.alpaca.markets"

stopLossMargin = 0.05 # percentage margin for the stop loss
# example: 10 - (10*0.05) = 9.5 means that my stoploss is at 9.5$

takeProfitMargin = 0.1 # percentage margin for the take profit
# example: 10 + (10*0.1) = 11 means that my take profit is at 11$

maxSpentEquity = 1000 # total equity to spend in a single operation

# MAX ATTEMPTS SECTION
maxAttemptCP = 5 # CHECK POSITION
maxAttemptGCP = 5 # GET CURRENT PRICE

# SLEEP TIMES SECTION
sleepTimeCP = 5 # CHECK POSITION
sleepTimeGCP = 5 # GET CURRENT PRICE
