# encoding: utf-8 

import logging
import os
from datetime import datetime

def initialize_logger() :

    # creating a folder for the logs
    logs_path = "./logs/"  # define the path
    try:
        os.mkdir(logs_path)
    except OSError:
        print("Creation of the directory %s failed - it does not have to be bad" % logs_path)    
    else:
        print("Successfully created log directory")

    # remaining each log depending on the time
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = date + '.log'
    currentLog_path = logs_path + log_name

    # log parameters
    logging.basicConfig(filename=currentLog_path, format="%(asctime)s - %(levelname)s: %(message)s",level=logging.DEBUG)
   
    # init message
    logging.info("Log Initialized!")
    

