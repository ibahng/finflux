from base_var import *
import yfinance as yf
import numpy as np
import requests
import pandas as pd
from datetime import timedelta
import math
import warnings
from typing import Union

class InvalidParameterError(Exception):
    def __init__(self, msg):
        self.msg = msg

class InvalidSecurityError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class forex:
    security_type = 'CURRENCY'

    def __init__(self,ticker):
        self.ticker = ticker

        self.from_currency = ticker[0:3]
        self.to_currency = ticker[3:6]

        if self.from_currency == 'USD':
            self.yfticker = f'{self.to_currency}=X'
        elif self.from_currency != 'USD':
            self.yfticker = f'{self.from_currency}{self.to_currency}=X'

        self.tdticker = f'{self.from_currency}/{self.to_currency}'

        instrumentType = yf.Ticker(self.yfticker).get_info()['quoteType']
        if instrumentType != forex.security_type:
            raise InvalidSecurityError(f"Invalid security type. "
                                       f"Please select a valid '{forex.security_type}' symbol")

    
    def timeseries(self, period: str = '5y', start: str = None, end: str = None, interval: str = '1d', data: str = 'all', calculation: str = 'price'):
        #Checking if the parameter inputs are invalid
        valid_params = {'valid_period' : ['1mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        'valid_interval' : ['1d', '1wk', '1mo', '3mo'],
                        'valid_data' : ['open', 'high', 'low', 'close', 'all'],
                        'valid_calculation' : ['price', 'simple return', 'log return']}
        
        params = {'period': period,
                  'interval': interval,
                  'data': data,
                  'calculation': calculation}
        
        #Raising an error if the parameter is invalid
        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        #Downloading the raw price data timeseries from yahoo finance with some presets'''
        #Note: The start, end parameters override the period parameter
        timeseries_data = yf.download(self.yfticker, period=period, start=start, end=end, interval=interval, ignore_tz=True, rounding=True, group_by='column', progress=False)

        #Deciding which columns of the raw price data to look at
        if data == 'all':
            timeseries_data = timeseries_data[['Open', 'High', 'Low', 'Close']]
        else:
            timeseries_data = timeseries_data[data.capitalize()]

        #Deciding between price data or percent return data
        if calculation == 'simple return':
            timeseries_data = (timeseries_data / timeseries_data.shift(1))-1
        elif calculation == 'log return':
            timeseries_data = np.log(timeseries_data / timeseries_data.shift(1))

        timeseries_data = timeseries_data.round(2)

        return timeseries_data

    def realtime(self, display: str = 'json'):
        valid_params = {'display': ['json', 'pretty']}

        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
        url = td_baseurl + f'price?apikey={td_apikey}&symbol={self.tdticker}'
        response = requests.get(url).json()
        
        output = {'symbol': self.ticker,
                  'price': float(response['price'])}

        if display == 'json':
            None
        elif display == 'pretty':
            output = f'''
       Symbol: {output['symbol']}
Exchange Rate: {output['price']}
'''
        return output
    
    def conversion(self, amount: int, rate: Union[int, float] = 'realtime', display: str = 'json'):
        valid_params = {'display': ['json', 'pretty']}

        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        if rate == 'realtime':
            conversion_rate = float(self.realtime()['price'])
        else:
            conversion_rate = rate

        post_conversion = conversion_rate * amount

        data = {
            'conversion': f'{self.ticker[0:3]} to {self.ticker[3:6]}',
            'exchange rate': conversion_rate,
            'pre-conversion': amount,
            'post-conversion': post_conversion
        }

        if display == 'json':
            return data
        if display == 'pretty':
            return f'''
     Conversion: {data['conversion']}
  Exchange Rate: {data['exchange rate']}
 Pre-conversion: {data['pre-conversion']}
Post-conversion: {round(data['post-conversion'],2)}
'''

    def quote(): # IN PROGRESS
        None

print(forex('USDKRW').timeseries())

print(forex('USDJPY').realtime(display='pretty'))

print(forex('USDEUR').conversion(display='pretty', amount=10000))