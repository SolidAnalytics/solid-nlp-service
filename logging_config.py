# logging_config.py

import logging

def setup_logging(log_file='app.log', level=logging.INFO):
    logging.basicConfig(
        filename=log_file,  
        level=level,  
        format='%(asctime)s - %(levelname)s - %(message)s',  
        datefmt='%Y-%m-%d %H:%M:%S'  
    )
