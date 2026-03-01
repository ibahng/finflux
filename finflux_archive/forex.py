from finflux.base_var import Config

import yfinance as yf # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore
from typing import Union

#------------------------------------------------------------------------------------------
class InvalidParameterError(Exception):
    def __init__(self, msg):
        self.msg = msg

class InvalidSecurityError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class MissingConfigObject(Exception):
    def __init__(self, msg: str):
        self.msg = msg

#------------------------------------------------------------------------------------------
class forex:
    security_type = 'CURRENCY'

    def __init__(self,ticker):
        self.ticker = ticker

        self.from_currency, self.to_currency = ticker.split('-')

        if self.from_currency == 'USD':
            self.yfticker = f'{self.to_currency}=X'
        elif self.from_currency != 'USD':
            self.yfticker = f'{self.from_currency}{self.to_currency}=X'

        self.tdticker = f'{self.from_currency}/{self.to_currency}'

        instrumentType = yf.Ticker(self.yfticker).get_info()['quoteType']
        if instrumentType != forex.security_type:
            raise InvalidSecurityError(f"Invalid security type. "
                                       f"Please select a valid '{forex.security_type}' symbol")
#------------------------------------------------------------------------------------------
    def help(self):
        output = '''
class forex():
 |  timeseries()------------Forex pair exchange rate timeseries
 |      period      :str        =5y         [1mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]
 |      start       :str        =None       [YYYY-MM-DD*]
 |      end         :str        =None       [YYYY-MM-DD*]
 |      interval    :str        =1d         [1d, 1wk, 1mo, 3mo]
 |      data        :str        =all        [open, high, low, close, all]
 |      calculation :str        =price      [price, simple return, log return]
 |      round       :bool       =True       [True, False]
 |      -----api(s): yfinance
 |
 |  realtime()--------------Forex pair realtime exchange rate
 |      display     :str        =json       [json, pretty]
 |      -----api(s): twelve data
 |      
 |  conversion()------------Forex pair currency conversion calculator
 |      display     :str        =json       [json, pretty]
 |      amount      :int        =None       [INT*]
 |      rate        :str, float =realtime   [realtime, eod, FLOAT*]
 |      -----api(s): yfinance, twelve data
 |      
 |  quote()-----------------Forex pair quote: EOD OHLCV, TTM high/low, percent change (5d, 1m, 6m, ytd, 1y, 5y), rate/volume SMAs
 |      display     :str        =json       [json, pretty]
 |      -----api(s): yfinance, twelve data
 |      
 |  news()------------------Forex pair related news
 |      display     :str        =json       [json, pretty]
 |      -----api(s): yfinance
'''

        print(output)
#------------------------------------------------------------------------------------------
    def timeseries(self, period: str = '5y', start: str = None, end: str = None, interval: str = '1d', data: str = 'all', calculation: str = 'price', round: bool = True): 
        valid_params = {'valid_period' : ['1mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        'valid_interval' : ['1d', '1wk', '1mo', '3mo'],
                        'valid_data' : ['open', 'high', 'low', 'close', 'all'],
                        'valid_calculation' : ['price', 'simple return', 'log return'],
                        'valid_round' : [True, False]}
        
        params = {'period': period,
                  'interval': interval,
                  'data': data,
                  'calculation': calculation,
                  'round': round}
        
        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        #RAW DATA/OBSERVATION--------------------------------------------------------------
        timeseries_data = yf.download(self.yfticker, period=period, start=start, end=end, interval=interval, ignore_tz=True, rounding=round, group_by='column', progress=False)
        #----------------------------------------------------------------------------------

        #PARAMETER - DATA =================================================================
        if data == 'all':
            timeseries_data = timeseries_data[['Open', 'High', 'Low', 'Close']]
        else:
            timeseries_data = timeseries_data[data.capitalize()]

        timeseries_data.columns = pd.MultiIndex.from_tuples([(col[0], f'{self.ticker}') for col in timeseries_data.columns])

        #PARAMETER - CALCULATION ==========================================================
        if calculation == 'price':
            output = timeseries_data
        if calculation == 'simple return':
            output = (timeseries_data / timeseries_data.shift(1))-1
        elif calculation == 'log return':
            output = np.log(timeseries_data / timeseries_data.shift(1))

        return output
#------------------------------------------------------------------------------------------
    def realtime(self, display: str = 'json'):
        valid_params = {'display': ['json', 'pretty']}

        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        if Config.td_apikey is None:
            raise MissingConfigObject('Missing td_apikey. Please set your Twelve Data api key using the set_config() function.')

        #RAW DATA/OBSERVATION--------------------------------------------------------------
        url = Config.td_baseurl + f'price?apikey={Config.td_apikey}&symbol={self.tdticker}'
        td_realtime = requests.get(url).json()
        #----------------------------------------------------------------------------------
        
        realtime_data = {
            'symbol': f'{self.from_currency} {self.to_currency}',
            'price': float(td_realtime['price'])
        }

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = realtime_data
            return output
        elif display == 'pretty':
            output = f'''
       Symbol: {realtime_data['symbol']}
Exchange Rate: {realtime_data['price']}
'''
            print(output)
#------------------------------------------------------------------------------------------    
    def conversion(self, display: str = 'json', amount: int = None, rate: Union[str, float] = 'realtime'):
        valid_params = {'display': ['json', 'pretty']}

        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #PARAMETER - RATE =================================================================
        if rate == 'realtime':
            conversion_rate = float(self.realtime()['price'])
        elif rate == 'eod':
            conversion_rate = round(yf.download(self.yfticker, progress=False)['Close'].iloc[-1].iloc[0],2)
        else:
            conversion_rate = rate

        #CALCULATION
        post_conversion = conversion_rate * amount

        #JSON FORMAT DATA
        data = {
            'conversion': f'{self.from_currency} to {self.to_currency}',
            'exchange rate': conversion_rate,
            'pre-conversion': amount,
            'post-conversion': post_conversion
        }

        #PARAMETER - DISPLAY =============================================================
        if display == 'json':
            output = data
            return output
        if display == 'pretty':
            output = f'''
     Conversion: {data['conversion']}
  Exchange Rate: {data['exchange rate']}
 Pre-conversion: {data['pre-conversion']}
Post-conversion: {round(data['post-conversion'],2)}
'''
            print(output)
#------------------------------------------------------------------------------------------
    def quote(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        if Config.td_apikey is None:
            raise MissingConfigObject('Missing td_apikey. Please set your Twelve Data api key using the set_config() function.')
        
        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        price_data = yf.download(self.yfticker, progress=False)

        yf_history_metadata = yf.Ticker(self.yfticker).get_history_metadata()
        
        url_1 = f'{Config.td_baseurl}quote?symbol={self.tdticker}&apikey={Config.td_apikey}'
        td_quote = requests.get(url_1).json()

        yf_eod = yf.download(self.yfticker, progress=False)['Close'].iloc[-1].iloc[0]

        current_year = pd.Timestamp.now().year
        #----------------------------------------------------------------------------------
        
        #JSON FORMAT DATA
        quote_data = {
            'symbol': td_quote.get('symbol', '-'),
            'name': td_quote.get('name', '-'),
            'exchange': td_quote.get('exchange', '-'),
            'timezone': yf_history_metadata.get('timezone','-'),
            'last trading day': {
                'date': str(price_data.index[-1].date()),
                'open': float((price_data['Open'].iloc[-1]).iloc[0]),
                'high': float((price_data['High'].iloc[-1]).iloc[0]),
                'low': float((price_data['Low'].iloc[-1]).iloc[0]),
                'close': float((price_data['Close'].iloc[-1]).iloc[0])
            },
            'ttm': {
                'high': round(float((price_data['High'].iloc[-252:].max()).iloc[0]),2),
                'low': round(float((price_data['Low'].iloc[-252:].min()).iloc[0]),2)
            },
            'percent change': {
                '5y': float(((yf_eod/price_data['Close'].iloc[-1260]) - 1).iloc[0]) if price_data.shape[0]>1260 else np.nan,
                '1y': float(((yf_eod/price_data['Close'].iloc[-252]) - 1).iloc[0]) if price_data.shape[0]>252 else np.nan,
                'ytd': float(((yf_eod/price_data['Close'][price_data.index.year == current_year].iloc[0]) - 1).iloc[0]),
                '6m': float(((yf_eod/price_data['Close'].iloc[-126]) - 1).iloc[0]) if price_data.shape[0]>126 else np.nan,
                '1m': float(((yf_eod/price_data['Close'].iloc[-21]) - 1).iloc[0]) if price_data.shape[0]>21 else np.nan,
                '5d': float(((yf_eod/price_data['Close'].iloc[-5]) - 1).iloc[0]) if price_data.shape[0]>5 else np.nan
            },
            '50d average price': float((price_data['Close'].iloc[-50:].mean()).iloc[0]),
            '200d average price': float((price_data['Close'].iloc[-200:].mean()).iloc[0])
        }

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = quote_data
            return output
        elif display == 'pretty':
            output = f'''
        Identifier: {quote_data['symbol']} - {quote_data['name']}
 Exchange/Timezone: {quote_data['exchange']} - {quote_data['timezone']}

{quote_data['last trading day']['date']} OHLCV------------------------
           OPEN --  {round(quote_data['last trading day']['open'],2):,}
           HIGH --  {round(quote_data['last trading day']['high'],2):,}
            LOW --  {round(quote_data['last trading day']['low'],2):,}
          CLOSE --  {round(quote_data['last trading day']['close'],2):,}
TTM HIGH/LOW----------------------------
           HIGH --  {round(quote_data['ttm']['high'],2):,}{'*' if price_data.shape[0]<252 else ''}
            LOW --  {round(quote_data['ttm']['low'],2):,}{'*' if price_data.shape[0]<252 else ''}
PERCENT CHANGE--------------------------
         5 YEAR -- {' ' if pd.isna(quote_data['percent change']['5y']) or quote_data['percent change']['5y']>0 else ''}{round(quote_data['percent change']['5y'] * 100,2)}%
         1 YEAR -- {' ' if pd.isna(quote_data['percent change']['1y']) or quote_data['percent change']['1y']>0 else ''}{round(quote_data['percent change']['1y'] * 100,2)}%
            YTD -- {' ' if pd.isna(quote_data['percent change']['ytd']) or quote_data['percent change']['ytd']>0 else ''}{round(quote_data['percent change']['ytd'] * 100,2)}%
        6 MONTH -- {' ' if pd.isna(quote_data['percent change']['6m']) or quote_data['percent change']['6m']>0 else ''}{round(quote_data['percent change']['6m'] * 100,2)}%
        1 MONTH -- {' ' if pd.isna(quote_data['percent change']['1m']) or quote_data['percent change']['1m']>0 else ''}{round(quote_data['percent change']['1m'] * 100,2)}%
          5 DAY -- {' ' if pd.isna(quote_data['percent change']['5d']) or quote_data['percent change']['5d']>0 else ''}{round(quote_data['percent change']['5d'] * 100,2)}%
MOVING AVERAGES-------------------------
   50 DAY PRICE --  {round(quote_data['50d average price'],2)}
  200 DAY PRICE --  {round(quote_data['200d average price'],2)}
'''
            print(output)
#------------------------------------------------------------------------------------------
    def news(self, display: str = 'json'): 
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATIONS---------------------------------------------------------
        news = yf.Ticker(self.yfticker).get_news()
        #------------------------------------------------------------------------------

        #JSON FORMAT DATA
        news_data = []
        for article in news:
            article = article['content']
            data_point = {
                'title': article['title'],
                'publish date': f'{article['pubDate'][0:10]} {article['pubDate'][11:19]}',
                'provider': article['provider']['displayName'],
                'snippet': article['summary'],
                'url': article['canonicalUrl']['url'],
            }
            news_data.append(data_point)

        #PARAMETER - DISPLAY ==========================================================
        if display == 'json':
            output = news_data
            return output
        if display == 'pretty':
            article_strings = '---------------------------------------------------------------------------------\n'
            
            for i in news_data:
                string = f'''{i['title']}
{i['provider']} -- {i['publish date']}

{i['snippet']}

URL: {i['url']}
---------------------------------------------------------------------------------\n'''
                article_strings += string

            output = article_strings

            print(output)
#------------------------------------------------------------------------------------------
