from datafetch.base_var import Config

import yfinance as yf # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore
from datetime import timedelta
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
class crypto:
    security_type = 'CRYPTOCURRENCY'

    def __init__(self,ticker):
        self.ticker = ticker
        self.from_coin, self.to_cc = ticker.split('-')

        self.yfticker = f'{self.from_coin}-USD'

        instrumentType = yf.Ticker(self.yfticker).get_info()['quoteType']
        if instrumentType != crypto.security_type:
            raise InvalidSecurityError(f"Invalid security type. "
                                       f"Please select a valid '{crypto.security_type}' symbol")
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
        timeseries_data = yf.download(f'{self.from_coin}-USD', period=period, start=start, end=end, interval=interval, ignore_tz=True, rounding=round, group_by='column', progress=False)
        #----------------------------------------------------------------------------------
        
        forex_start = str(timeseries_data.index[0] + timedelta(days=-5))[0:10]
        forex_end = str(timeseries_data.index[-1])[0:10]
        
        if self.to_cc == 'USD':
            timeseries_data = timeseries_data
        if self.to_cc != 'USD':
            other_timeseries_data = yf.download(f'{self.from_coin}-{self.to_cc}', period=period, start=start, end=end, interval=interval, ignore_tz=True, rounding=True, group_by='column', progress=False)
            
            if not other_timeseries_data.empty:
                timeseries_data = other_timeseries_data

            elif other_timeseries_data.empty:
                yf_forex_timeseries = yf.download(f'{self.to_cc}=X', progress=False, start=forex_start, end=forex_end)['Close']

                missing_index = yf_forex_timeseries.index.difference(timeseries_data.index)

                timeseries_data = timeseries_data.reindex(timeseries_data.index.union(missing_index))

                #adding the forex exchange rates closes with USD as base
                timeseries_data[('Close', f'USD-{self.to_cc}')] = yf_forex_timeseries

                #forward filling in the missing forex exchange rates in the weekends and holidays
                timeseries_data[('Close', f'USD-{self.to_cc}')] = timeseries_data[('Close', f'USD-{self.to_cc}')].ffill()

                #creating the new columns of coin exchange rate in missing currencies
                timeseries_data[('Close', f'{self.from_coin}-{self.to_cc}')] = timeseries_data[('Close', f'{self.from_coin}-USD')] * timeseries_data [('Close', f'USD-{self.to_cc}')]
                timeseries_data[('High', f'{self.from_coin}-{self.to_cc}')] = timeseries_data[('High', f'{self.from_coin}-USD')] * timeseries_data [('Close', f'USD-{self.to_cc}')]
                timeseries_data[('Low', f'{self.from_coin}-{self.to_cc}')] = timeseries_data[('Low', f'{self.from_coin}-USD')] * timeseries_data [('Close', f'USD-{self.to_cc}')]
                timeseries_data[('Open', f'{self.from_coin}-{self.to_cc}')] = timeseries_data[('Open', f'{self.from_coin}-USD')] * timeseries_data [('Close', f'USD-{self.to_cc}')]

                #deleteing original USD based coin exchange rates used in the calculations
                del timeseries_data[('Close', f'{self.from_coin}-USD')]
                del timeseries_data[('High', f'{self.from_coin}-USD')]
                del timeseries_data[('Low', f'{self.from_coin}-USD')]
                del timeseries_data[('Open', f'{self.from_coin}-USD')]
                del timeseries_data[('Volume', f'{self.from_coin}-USD')]
                del timeseries_data[('Close', f'USD-{self.to_cc}')]

                timeseries_data = timeseries_data.dropna()

        #PARAMETER - DATA =================================================================
        if data == 'all':
            timeseries_data = timeseries_data[['Close', 'High', 'Low', 'Open']]
        else:
            timeseries_data = timeseries_data[data.capitalize()]

        #PARAMETER - CALCULATION ==========================================================NOT WORKING
        if calculation == 'price':
            output = timeseries_data
        if calculation == 'simple return':
            output = (timeseries_data / timeseries_data.shift(1))-1
        elif calculation == 'log return':
            output = np.log(timeseries_data / timeseries_data.shift(1))

        #rounding to 2 decimals
        output = timeseries_data.round(2)

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
        url_1 = 'https://api.twelvedata.com/cryptocurrencies'
        td_crypto_json = requests.get(url_1).json()['data']

        td_crypto_list = []
        for i in td_crypto_json:
            a = i['symbol']
            td_crypto_list.append(a)

        #retriving coin exchange rate if directly avaliable
        if f'{self.from_coin}/{self.to_cc}' in td_crypto_list:
            url_2 = Config.td_baseurl + f'price?apikey={Config.td_apikey}&symbol={self.from_coin}/{self.to_cc}'
            td_realtime = float(requests.get(url_2).json()['price'])

        #calculating coin exchange rate by passing through USD rates
        elif f'{self.from_coin}/{self.to_cc}' not in td_crypto_list:
            url_2 = Config.td_baseurl + f'price?apikey={Config.td_apikey}&symbol={self.from_coin}/USD'
            td_realtime_coinusd = float(requests.get(url_2).json()['price'])

            url_3 = Config.td_baseurl + f'price?apikey={Config.td_apikey}&symbol=USD/{self.to_cc}'
            td_realtime_usdcc = float(requests.get(url_3).json()['price'])

            td_realtime = td_realtime_coinusd * td_realtime_usdcc
        #----------------------------------------------------------------------------------
        
        #JSON FORMAT DATA
        realtime_data = {
            'symbol': self.ticker,
            'price': td_realtime
        }

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = realtime_data
            return output
        elif display == 'pretty':
            output = f'''
       Symbol: {realtime_data['symbol']}
Exchange Rate: {realtime_data['price']:2f}
'''
            print(output)
#------------------------------------------------------------------------------------------    
    def conversion(self, amount: int, rate: Union[int, float] = 'realtime', display: str = 'json'):
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
            conversion_rate = round(crypto(self.ticker).timeseries()['Close'].iloc[-1].iloc[0],2)
        else:
            conversion_rate = rate

        #CALCULATION
        post_conversion = conversion_rate * amount

        #JSON FORMAT DATA
        data = {
            'conversion': f'{self.from_coin} to {self.to_cc}',
            'exchange rate': conversion_rate,
            'pre-conversion': amount,
            'post-conversion': post_conversion
        }

        #PARAMETER - DISPLAY =============================================================
        if display == 'json':
            output = data
            return output
        if display == 'pretty':
            output =f'''
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

        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_download = crypto(self.ticker).timeseries(period='max')

        yf_history_metadata = yf.Ticker(self.ticker).get_history_metadata()

        yf_eod = yf_download['Close'].iloc[-1].iloc[0]

        current_year = pd.Timestamp.now().year
        #----------------------------------------------------------------------------------
        
        #JSON FORMAT DATA
        quote_data = {
            'symbol': yf_history_metadata.get('symbol', f'{self.ticker}'),
            'name': yf_history_metadata.get('longName', '-'),
            'exchange': yf_history_metadata.get('exchangeName', '-'),
            'timezone': yf_history_metadata.get('timezone','-'),
            'last trading day': {
                'date': str(yf_download.index[-1].date()),
                'open': float((yf_download['Open'].iloc[-1]).iloc[0]),
                'high': float((yf_download['High'].iloc[-1]).iloc[0]),
                'low': float((yf_download['Low'].iloc[-1]).iloc[0]),
                'close': float((yf_download['Close'].iloc[-1]).iloc[0])
            },
            'ttm': {
                'high': round(float((yf_download['High'].iloc[-252:].max()).iloc[0]),2),
                'low': round(float((yf_download['Low'].iloc[-252:].min()).iloc[0]),2)
            },
            'percent change': {
                '5y': float(((yf_eod/yf_download['Close'].iloc[-1260]) - 1).iloc[0]) if yf_download.shape[0]>1260 else np.nan,
                '1y': float(((yf_eod/yf_download['Close'].iloc[-252]) - 1).iloc[0]) if yf_download.shape[0]>252 else np.nan,
                'ytd': float(((yf_eod/yf_download['Close'][yf_download.index.year == current_year].iloc[0]) - 1).iloc[0]),
                '6m': float(((yf_eod/yf_download['Close'].iloc[-126]) - 1).iloc[0]) if yf_download.shape[0]>126 else np.nan,
                '1m': float(((yf_eod/yf_download['Close'].iloc[-21]) - 1).iloc[0]) if yf_download.shape[0]>21 else np.nan,
                '5d': float(((yf_eod/yf_download['Close'].iloc[-5]) - 1).iloc[0]) if yf_download.shape[0]>5 else np.nan
            },
            '50d average price': float((yf_download['Close'].iloc[-50:].mean()).iloc[0]),
            '200d average price': float((yf_download['Close'].iloc[-200:].mean()).iloc[0])
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
           HIGH --  {round(quote_data['ttm']['high'],2):,}{'*' if yf_download.shape[0]<252 else ''}
            LOW --  {round(quote_data['ttm']['low'],2):,}{'*' if yf_download.shape[0]<252 else ''}
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
        news = yf.Ticker(self.ticker).get_news()
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
