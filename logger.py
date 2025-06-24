import logging
from config import LOG_FILE

# Configuration du journal
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log(message):
    logging.info(message)