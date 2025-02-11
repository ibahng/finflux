from base_var import *
import yfinance as yf
import numpy as np
import requests
import pandas as pd
from datetime import timedelta
import math
import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning)

class InvalidParameterError(Exception):
    def __init__(self, msg):
        self.msg = msg

class InvalidSecurityError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class bond: #need to create structure outline
    security_type_1 = 'ETF'

    def __init__(self,ticker):
        self.ticker = ticker

        instrumentType = yf.Ticker(self.ticker).get_history_metadata()['instrumentType']
        if instrumentType != bond.security_type_1 or instrumentType != bond.security_type_2:
            raise InvalidSecurityError(f"Invalid security type. "
                                       f"Please select a valid '{bond.security_type_1}' or  '{bond.security_type_2}'symbol")
        
    def timeseries():
        pass

    def realtime():
        pass

    def holdings():
        pass

    def asset_class():
        pass
    
    def overview():
        pass