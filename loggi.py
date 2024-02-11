import logging as lg
import os
from datetime import datetime

def initialize_logger(logs_path='./logs/'):
    """
    Initializes logger configuration.

    Args:
    logs_path (str): Path to the directory where logs will be stored. Defaults to './logs/'.
    """

    # Create a folder for the logs if it doesn't exist
    try:
        os.makedirs(logs_path, exist_ok=True)
        print("Successfully created log directory")
    except OSError as e:
        print(f"Creation of the directory {logs_path} failed: {e}")
    
    # Generate log file with timestamped name
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = date + '.log'
    current_log_path = os.path.join(logs_path, log_name)

    # Configure log parameters
    lg.basicConfig(filename=current_log_path, format="%(asctime)s - %(levelname)s: %(message)s", level=lg.DEBUG)
    
    # Initialize logger
    lg.info("Log Initialized!")

    # Add console handler for logging
    console_handler = lg.StreamHandler()
    console_handler.setLevel(lg.INFO)  # Set console logging level
    formatter = lg.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    lg.getLogger().addHandler(console_handler)

# Example usage:
initialize_logger()
lg.debug("Debug message")
lg.info("Info message")
lg.warning("Warning message")
lg.error("Error message")
lg.critical("Critical message")
