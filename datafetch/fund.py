from datafetch.base_var import Config

import yfinance as yf # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore

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
class fund:
    security_type_1 = 'ETF'
    security_type_2 = 'MUTUALFUND'

    def __init__(self,ticker):
        self.ticker = ticker

        quoteType = yf.Ticker(self.ticker).get_info()['quoteType']
        if quoteType != fund.security_type_1 and quoteType != fund.security_type_2:
            raise InvalidSecurityError(f"Invalid security type. "
                                       f"Please select a valid '{fund.security_type_1}' or '{fund.security_type_2}' symbol")
#------------------------------------------------------------------------------------------
    def help(self):
        output = '''
class fund():
 |  timeseries()------------OHLC fund price daily timeseries
 |      period      :str        =5y         [1mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]
 |      start       :str        =None       [YYYY-MM-DD*]
 |      end         :str        =None       [YYYY-MM-DD*]
 |      interval    :str        =1d         [1d, 1wk, 1mo, 3mo]
 |      data        :str        =all        [open, high, low, close, all]
 |      round       :bool       =True       [True, False]
 |      -----api(s): yfinance
 |
 |  eod()-------------------End of day fund price
 |      display     :str        =json       [json, pretty]
 |      -----api(s): yfinance
 |      
 |  equity_holdings()-------Top ten equity holdings
 |      display     :str        =json       [json, table]
 |      -----api(s): yfinance
 |      
 |  info()------------------General fund info: sector weighting, asset classes, etc.
 |      display     :str        =json       [json, pretty]
 |      -----api(s): yfinance, SEC
 |      
 |  news()------------------Fund related news
 |      display     :str        =json       [json, pretty]
 |      -----api(s): yfinance
 |
 |  quote()-----------------Fund quote: EOD OHLCV, TTM high/low, percent change (5d, 1m, 6m, ytd, 1y, 5y), price/volume SMAs
 |      display     :str        =json       [json, pretty]
 |      -----api(s): yfinance
 |
 |  split()-----------------Fund split timeseries
 |      display     :str        =json       [json, table]
 |      -----api(s): yfinance
 |
 |  dividend()--------------Fund dividend timeseries
 |      display     :str        =json       [json, table]
 |      -----api(s): yfinance
'''

        print(output)
#------------------------------------------------------------------------------------------
    def timeseries(self, period: str = '5y', start: str = None, end: str = None, interval: str = '1d', data: str = 'all', calculation: str = 'price', round: bool = True):
        valid_params = {'valid_period' : ['1mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        'valid_interval' : ['1d', '1wk', '1mo', '3mo'],
                        'valid_data' : ['open', 'high', 'low', 'close', 'volume', 'all'],
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

        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        #Downloading the raw price data timeseries from yahoo finance with some presets'''
        #Note: The start, end parameters override the period parameter
        yf_download = yf.download(self.ticker, period=period, start=start, end=end, interval=interval, ignore_tz=True, rounding=round, group_by='column', progress=False)
        #----------------------------------------------------------------------------------

        #PARAMETER - DATA =================================================================
        if data == 'all':
            yf_download = yf_download
        else:
            yf_download = yf_download[data.capitalize()]

        #PARAMETER - CALCULATION ==========================================================
        if calculation == 'price':
            output = yf_download
        if calculation == 'simple return':
            output = (yf_download / yf_download.shift(1))-1
        elif calculation == 'log return':
            output = np.log(yf_download / yf_download.shift(1))

        return output
#------------------------------------------------------------------------------------------
    def eod(self, display: str = 'json'):
        valid_params = {'display': ['json', 'pretty']}

        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_download = yf.download(self.ticker, period='1mo', progress=False)

        yf_info = yf.Ticker(self.ticker).get_info()
        #----------------------------------------------------------------------------------

        eod = yf_download['Close'].iloc[-1].iloc[0]
        
        #JSON FORMAT DATA
        eod_data = {'symbol': self.ticker,
                    'eod price': float(eod),
                    'currency': yf_info['currency']}

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = eod_data
            return output
        elif display == 'pretty':
            output = f'''  Symbol: {self.ticker}
   Price: {eod_data['eod price']:.2f}
Currency: {eod_data['currency']}'''
            print(output)
#------------------------------------------------------------------------------------------
    def equity_holdings(self, display: str = 'json'): 
        valid_params = {'display': ['json', 'table']}

        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_top_holdings = yf.Ticker(self.ticker).get_funds_data().top_holdings
        #----------------------------------------------------------------------------------

        #ADDING 6MO RETURN COLUMN
        def six_month_return(ticker):
            data = yf.download(ticker, period='6mo', progress=False)['Close']
            raw = (data.iloc[-1].iloc[0]/data.iloc[0].iloc[0]) - 1
            six_mo = str(round(raw * 100,2)) + '%'
            return six_mo

        yf_top_holdings['Holding Percent'] = (round(yf_top_holdings['Holding Percent']*100,2)).astype(str)

        yf_top_holdings['Holding Percent'] = yf_top_holdings['Holding Percent'].map(lambda x: f'{x}%')

        yf_top_holdings['6MO Return'] = yf_top_holdings.index.map(lambda x: six_month_return(x))

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = yf_top_holdings.to_dict(orient='index ')
            return output
        if display == 'table':
            output = yf_top_holdings
            return output
#------------------------------------------------------------------------------------------    
    def info(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        if Config.email_address is None:
            raise MissingConfigObject('Missing email_address. Please set your email address using the set_config() function.')
        
        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_info = yf.Ticker(self.ticker).get_info()

        yf_sector_weights = yf.Ticker(self.ticker).get_funds_data().sector_weightings

        yf_fund_operations = yf.Ticker(self.ticker).get_funds_data().fund_operations

        yf_asset_classes = yf.Ticker(self.ticker).get_funds_data().asset_classes

        #cik id
        sec_headers = {'User-Agent': f"{Config.email_address}"}
        sec_list = requests.get("https://www.sec.gov/files/company_tickers.json", headers=sec_headers).json()

        companyData = pd.DataFrame.from_dict(sec_list, orient='index')

        companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)

        try:
            index_of_ticker = int(companyData[companyData['ticker'] == self.ticker].index[0])

            cik = companyData.iloc[index_of_ticker,0]
        except IndexError:
            cik = '-'
        #----------------------------------------------------------------------------------

        #JSON FORMAT DATA
        info_data = {
            'symbol': yf_info.get('symbol', '-'),
            'name': yf_info.get('longName', '-'),
            'exchange': yf_info.get('exchange', '-'),
            'stock currency': yf_info.get('currency', '-'),
            'timezone': yf_info.get('timeZoneShortName', '-'),
            'cik': cik,
            'description': yf_info.get('longBusinessSummary', '-'),
            'sector weights': yf_sector_weights,
            'total net assets': yf_fund_operations[self.ticker].loc['Total Net Assets'],
            'asset classes': yf_asset_classes
        }

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = info_data
            return output
        elif display == 'pretty':
            output = f'''
        Identifier: {info_data['symbol']} - {info_data['name']}
 Exchange/Timezone: {info_data['exchange']} - {info_data['timezone']}
    Stock Currency: {info_data['stock currency']}
               CIK: {info_data['cik']}
  Total Net Assets: {int(info_data['total net assets']) if isinstance(info_data['total net assets'], (int, float)) else '-'}

DESCRIPTION-------------------------------------------------------
{info_data['description']}

SECTOR WEIGHTING--------------------------------------------------
           Real Estate -- {info_data['sector weights']['realestate']*100:.2f}%
     Consumer Cyclical -- {info_data['sector weights']['consumer_cyclical']*100:.2f}%
       Basic Materials -- {info_data['sector weights']['basic_materials']*100:.2f}%
    Consumer Defensive -- {info_data['sector weights']['consumer_defensive']*100:.2f}%
            Technology -- {info_data['sector weights']['technology']*100:.2f}%
Communication Services -- {info_data['sector weights']['communication_services']*100:.2f}%
    Financial Services -- {info_data['sector weights']['financial_services']*100:.2f}%
             Utilities -- {info_data['sector weights']['utilities']*100:.2f}%
           Industrials -- {info_data['sector weights']['industrials']*100:.2f}%
                Energy -- {info_data['sector weights']['energy']*100:.2f}%
            Healthcare -- {info_data['sector weights']['healthcare']*100:.2f}%

ASSET CLASSES-----------------------------------------------------
                  Cash -- {info_data['asset classes']['cashPosition']*100:.2f}%
                 Stock -- {info_data['asset classes']['stockPosition']*100:.2f}%
                  Bond -- {info_data['asset classes']['bondPosition']*100:.2f}%
             Preferred -- {info_data['asset classes']['preferredPosition']*100:.2f}%
           Convertible -- {info_data['asset classes']['convertiblePosition']*100:.2f}%
                 Other -- {info_data['asset classes']['otherPosition']*100:.2f}%
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
        
        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_news = yf.Ticker(self.ticker).get_news()
        #----------------------------------------------------------------------------------

        #JSON FORMAT DATA
        news_data = []

        for article in yf_news:
            article = article['content']
            data_point = {
                'title': article['title'],
                'publish date': f'{article['pubDate'][0:10]} {article['pubDate'][11:19]}',
                'provider': article['provider']['displayName'],
                'snippet': article['summary'],
                'url': article['canonicalUrl']['url'],
            }
            news_data.append(data_point)

        #PARAMETER - DISPLAY ==============================================================
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
    def quote(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_download = yf.download(self.ticker, progress=False, period='10y')
        
        yf_info = yf.Ticker(self.ticker).get_info()
        
        eod_price = fund(self.ticker).eod()['eod price']

        current_year = pd.Timestamp.now().year
        #----------------------------------------------------------------------------------
        
        #JSON FORMAT DATA
        quote_data = {
            'symbol': yf_info.get('symbol', '-'),
            'name': yf_info.get('longName', '-'),
            'exchange': yf_info.get('exchange', '-'),
            'currency': yf_info.get('currency', '-'),
            'timezone': yf_info.get('timeZoneShortName','-'),
            'last trading day': {
                'date': str(yf_download.index[-1].date()),
                'open': float((yf_download['Open'].iloc[-1]).iloc[0]),
                'high': float((yf_download['High'].iloc[-1]).iloc[0]),
                'low': float((yf_download['Low'].iloc[-1]).iloc[0]),
                'close': float((yf_download['Close'].iloc[-1]).iloc[0]),
                'volume': int((yf_download['Volume'].iloc[-1]).iloc[0])
            },
            'ttm': {
                'high': round(float((yf_download['High'].iloc[-252:].max()).iloc[0]),2),
                'low': round(float((yf_download['Low'].iloc[-252:].min()).iloc[0]),2)
            },
            'percent change': {
                '5y': float(((eod_price/yf_download['Close'].iloc[-1260]) - 1).iloc[0]) if yf_download.shape[0]>1260 else np.nan,
                '1y': float(((eod_price/yf_download['Close'].iloc[-252]) - 1).iloc[0]) if yf_download.shape[0]>252 else np.nan,
                'ytd': float(((eod_price/yf_download['Close'][yf_download.index.year == current_year].iloc[0]) - 1).iloc[0]),
                '6m': float(((eod_price/yf_download['Close'].iloc[-126]) - 1).iloc[0]) if yf_download.shape[0]>126 else np.nan,
                '1m': float(((eod_price/yf_download['Close'].iloc[-21]) - 1).iloc[0]) if yf_download.shape[0]>21 else np.nan,
                '5d': float(((eod_price/yf_download['Close'].iloc[-5]) - 1).iloc[0]) if yf_download.shape[0]>5 else np.nan
            },
            '50d average price': float((yf_download['Close'].iloc[-50:].mean()).iloc[0]),
            '200d average price': float((yf_download['Close'].iloc[-200:].mean()).iloc[0]),
            '10d average volume': int((yf_download['Volume'].iloc[-10:].mean()).iloc[0]),
            '90d average volume': int((yf_download['Volume'].iloc[-90:].mean()).iloc[0]),
        }

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = quote_data
            return output
        elif display == 'pretty':
            output = f'''
        Identifier: {quote_data['symbol']} - {quote_data['name']}
 Exchange/Timezone: {quote_data['exchange']} - {quote_data['timezone']}
          Currency: {quote_data['currency']}

{quote_data['last trading day']['date']} OHLCV------------------------
           OPEN --  {round(quote_data['last trading day']['open'],2):,}
           HIGH --  {round(quote_data['last trading day']['high'],2):,}
            LOW --  {round(quote_data['last trading day']['low'],2):,}
          CLOSE --  {round(quote_data['last trading day']['close'],2):,}
         VOLUME --  {'{:,}'.format(round(quote_data['last trading day']['volume'],2))}
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
  10 DAY VOLUME --  {'{:,}'.format(quote_data['10d average volume'])}
  90 DAY VOLUME --  {'{:,}'.format(quote_data['90d average volume'])}
'''
            print(output)
#------------------------------------------------------------------------------------------
    def split(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'table'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_splits = yf.Ticker(self.ticker).get_splits()
        #----------------------------------------------------------------------------------

        renamed_dates = {}
        for i in yf_splits.keys():
            renamed_dates[i] = str(i)[0:10]

        yf_splits = yf_splits.rename(renamed_dates)

        splits_dict = yf_splits.to_dict()

        splits_df = pd.DataFrame.from_dict(splits_dict, orient='index', columns=['Splits'])

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = splits_dict
            return splits_dict
        elif display == 'table':
            output = splits_df
            return splits_df
#------------------------------------------------------------------------------------------
    def dividend(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'table'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
    
        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        yf_dividends = yf.Ticker(self.ticker).get_dividends()
        #----------------------------------------------------------------------------------

        renamed_dates = {}
        for i in yf_dividends.keys():
            renamed_dates[i] = str(i)[0:10]

        #renaming the datetime indexes to date
        yf_dividends = yf_dividends.rename(renamed_dates)

        #converting series to dict to dataframe
        dividends_dict = yf_dividends.to_dict()
        dividends_df = pd.DataFrame.from_dict(dividends_dict, orient='index', columns=['Dividends'])

        #making all values two decimal points
        dividends_df = dividends_df.map(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x)

        #PARAMETER - DISPLAY ==============================================================
        if display == 'json':
            output = dividends_dict
            return output
        elif display == 'table':
            output = dividends_df
            return output
#------------------------------------------------------------------------------------------
