"""

    Wallet Manager Library

"""
import logging
import sys



__version__ = '0.0.1'

LOGGER_NAME = 'wallet_manager'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(LOGGER_NAME)
