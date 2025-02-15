from base_var import *
import yfinance as yf # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore
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