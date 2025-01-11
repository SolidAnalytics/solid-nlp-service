# logging_config.py

import logging

def setup_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log"),
                logging.StreamHandler()
            ]
        )