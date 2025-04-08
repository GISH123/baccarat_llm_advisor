# src/utils.py
import logging
import os
from datetime import datetime

def setup_logging(log_directory="logs",model_name=None):
    """Set up logging to file and console."""
    os.makedirs(log_directory, exist_ok=True)
    log_filename = f"{log_directory}/output_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log" if model_name else f"{log_directory}/output.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )