# define asset
    # IN: keyboard
    # OUT: string

# LOOP until timeout reached (ex. 2h)
# POINT "ECHO": INITIAL CHECK --- coming to "ECHO"

# Check the Position : Ask the broker/API if we have an open position with "ASSET"
    # IN: asset (string)
    # OUT: True (exists) / False (does not exist)

# Check if Tradable : Ask the broker/API if "ASSET" is tradable
    # IN: asset (string)
    # OUT: True (exists) / False (does not exist)

# GENERAL TREND CHECK
# Load 30 - Min Candle : demand the API the 30-Min candles
    # IN: asset (whatever API needs), time range*,candle size*
    # OUT : 30-Min candles (OHLC for every candle)

# perform General Trend analysis: detect interesting trend (UP / DOWN / NO TREND) 
    # IN: 30_Min candles data (Close data)
    # OUT: UP / DOWN / NO TREND (strings)
  # ---if NO TREND go back to "ECHO"

    # LOOP_1 until timeout reached (ex. 30min) 
    # POINT "DELTA"

    # STEP 1: Load 5 - Min Candle
        # IN: asset (whatever API needs), time range*,candle size*
        # OUT : 5-Min candles (OHLC for every candle)
        # --- go back to POINT "DELTA"
    # STEP 2: Perform Instant Trend analysis: confirm the trend detected by GT analysis
        # IN: 5 - Min candles date (Close data), output of the GT analysis (UP / DOWN string)
        # OUT: True (confirmed) / False (not confirmed)
        # --- go back to POINT "DELTA"
    # STEP 3: Perform RSI analysis
        # IN: 5 - Min candles date (Close data), output of the GT analysis (UP / DOWN string)
        # OUT: True (confirmed) / False (not confirmed)
        # --- go back to POINT "DELTA"
    # STEP 4: Perform stochastic analysis
        # IN: 5 - Min candles date (OHLC data), output of the GT analysis (UP / DOWN string)
        # OUT: True (confirmed) / False (not confirmed)
        # --- go back to POINT "DELTA"

# SUBMIT ORDER
# Submit Order (limit order): interact with broker API
    # IN: # number of shares to operate with, asset, desired price
    # OUT: True (confirmed) / False (not confirmed), position ID
    # if false, abort / go back to POINT ECHO

# Check the Position: see if the position exists
    # IN: position ID
    # OUT: True (confirmed) / False (not confirmed), position ID
    # if false, abort / go back to POINT ECHO

# LOOP_1 until timeout reached (ex. ~8h)
# "ENTER POSITION " MODE: check the condition in PARALLEL (LOOP_2) ---if not go to 1
# IF Check Take Profit, if True -> close position
    # IN: current gains (earning $)
    # OUT: True / False

# ELIF Check Stop Loss, if True -> close position
    # IN: current gains (loosing $)
    # OUT: True / False

# ELIF Check Stochastic Crossing,Pull 5 OHLC data. if True -> close position
    # STEP 1: pull 5 minutes OHLC data.
        # IN: asset
        # OUT: OHLC data (5min candles)

    # STEP 2: see whether the stochastic curves are crossing
        # IN: OHLC data (5min candles)
        # OUT: True / False

# GET OUT
# Submit Order (market order): interact with broker API
    # IN: # number of shares to operate with, asset, position ID
    # OUT: True (confirmed) / False (not confirmed)
    # if false, retry until it works

# Check the Position: see if the position exists
    # IN: position ID
    # OUT: True (still exists!) / False (does not exist), position ID
    # if false, abort / go back to SUBMIT ORDER

# wait 15 min

# END


