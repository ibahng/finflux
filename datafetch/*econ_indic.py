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

class econ_indic: #need to create structure outline
    
    def gdp():
        pass

    def unemployment():
        pass

    def cpi():
        pass

    def ir():
        pass

    def sentiment():
        pass