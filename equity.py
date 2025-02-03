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


class equity:
    security_type = 'EQUITY'

    def __init__(self,ticker):
        self.ticker = ticker
        self.mticker = ticker.split('.')[0]

        instrumentType = yf.Ticker(self.ticker).get_history_metadata()['instrumentType']
        if instrumentType != equity.security_type:
            raise InvalidSecurityError(f"Invalid security type. "
                                       f"Please select a valid '{equity.security_type}' symbol")

    def timeseries(self, period: str = '5y', start: str = None, end: str = None, interval: str = '1d', data: str = 'all', calculation: str = 'price'):
        #Checking if the parameter inputs are invalid
        valid_params = {'valid_period' : ['1mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        'valid_interval' : ['1d', '1wk', '1mo', '3mo'],
                        'valid_data' : ['open', 'high', 'low', 'close', 'volume', 'all'],
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
        timeseries_data = yf.download(self.ticker, period=period, start=start, end=end, interval=interval, ignore_tz=True, rounding=True, group_by='column', progress=False)

        #Deciding which columns of the raw price data to look at
        if data == 'all':
            timeseries_data = timeseries_data
        else:
            timeseries_data = timeseries_data[data.capitalize()]

        #Deciding between price data or percent return data
        if calculation == 'simple return':
            timeseries_data = (timeseries_data / timeseries_data.shift(1))-1
        elif calculation == 'log return':
            timeseries_data = np.log(timeseries_data / timeseries_data.shift(1))

        return timeseries_data

    def realtime(self, display: str = 'json'):
        valid_params = {'display': ['json', 'pretty']}

        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
        url_1 = td_baseurl + f'price?apikey={td_apikey}&symbol={self.mticker}'
        response_1 = requests.get(url_1).json()

        url_2 = td_baseurl + f'quote?apikey={td_apikey}&symbol={self.mticker}'
        response_2 = requests.get(url_2).json()
        
        if display == 'json':
            output = {'symbol': self.ticker,
                      'price': float(response_1['price']),
                      'currency': response_2['currency']}
        elif display == 'pretty':
            output = f'''
  Symbol: {self.ticker}
   Price: {round(response_1['price'],2)}
Currency: {response_2['currency']}
'''

        return output
            
    def statement(self, statement: str = 'all', currency: str = None, unit: str = 'raw', display: str = 'json', decimal: bool = False, interval:str = 'annual'):
        valid_params = {'valid_statement' : ['income', 'balance', 'cash', 'all'],
                        'valid_unit' : ['thousand', 'million', 'billion', 'raw'],
                        'valid_display' : ['json', 'table'],
                        'valid_decimal' : [True, False],
                        'valid_interval' : ['annual', 'quarter']}
        
        params = {'statement': statement,
                  'units': unit,
                  'display': display,
                  'decimal': decimal,
                  'interval': interval}
        
        #Raising an error if the parameter is invalid
        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        firm = yf.Ticker(self.ticker)

        #STATEMENT ITEM CURRENCY
        current_currency = firm.get_info()['financialCurrency'] if 'financialCurrency' in firm.get_info().keys() else '---'

        #STATEMENT ITEMS
        statement_items = {
            'income': ['Total Revenue',
                       'Cost Of Revenue',
                       'Gross Profit',
                       'Research And Development',
                       'Other Operating Expenses',
                       'EBITDA',
                       'Reconciled Depreciation',
                       'EBIT',
                       'Interest Expense',
                       'Interest Income',
                       'Pretax Income',
                       'Tax Provision',
                       'Net Income'],
            'balance': ['Total Assets',
                        'Current Assets',
                        'Cash And Cash Equivalents',
                        'Accounts Receivable',
                        'Inventory',
                        'Other Current Assets',
                        'Total Non Current Assets',
                        'Net PPE',
                        'Goodwill And Other Intangible Assets',
                        'Other Non Current Assets',
                        'Total Liabilities Net Minority Interest',
                        'Current Liabilities',
                        'Accounts Payable',
                        'Current Debt And Capital Lease Obligation',
                        'Other Current Liabilities',
                        'Total Non Current Liabilities Net Minority Interest',
                        'Long Term Debt And Capital Lease Obligation',
                        'Other Non Current Liabilities',
                        'Total Equity Gross Minority Interest',
                        'Retained Earnings',
                        'Other Equity'],
            'cash': ['Operating Cash Flow',
                     'Net Income From Continuing Operations',
                     'Depreciation Amortization Depletion',
                     'Change In Working Capital',
                     'Other Operating Cash Flow',
                     'Investing Cash Flow',
                     'Capital Expenditure',
                     'Other Investing Cash Flow',
                     'Financing Cash Flow',
                     'Net Issuance Payments Of Debt',
                     'Net Common Stock Issuance',
                     'Cash Dividends Paid',
                     'Other Financing Cash Flow',
                     'Beginning Cash Position',
                     'Changes In Cash',
                     'Other Changes',
                     'End Cash Position']
        }

        renamed_items = {
            'income': ['Total Revenue',
                       'Cost Of Revenue',
                       'Gross Profit',
                       'Research And Development',
                       'Other Operating Expenses',
                       'EBITDA',
                       'Depreciation and Amortization',
                       'EBIT',
                       'Interest Expense',
                       'Interest Income',
                       'Pretax Income',
                       'Tax Provision',
                       'Net Income'],
            'balance': ['Total Assets',
                        'Total Current Assets',
                        'Cash And Cash Equivalents',
                        'Accounts Receivable',
                        'Inventory',
                        'Other Current Assets',
                        'Total Non Current Assets',
                        'Net PPE',
                        'Goodwill And Other Intangible Assets',
                        'Other Non Current Assets',
                        'Total Liabilities',
                        'Total Current Liabilities',
                        'Accounts Payable',
                        'Short Term Debt And Capital Lease Obligation',
                        'Other Current Liabilities',
                        'Total Non Current Liabilities',
                        'Long Term Debt And Capital Lease Obligation',
                        'Other Non Current Liabiltiies',
                        'Total Equity',
                        'Retained Earnings',
                        'Other Equity'],
            'cash': ['Operating Cash Flow',
                     'Net Income',
                     'Depreciation And Amortization',
                     'Change In Working Capital',
                     'Other Operating Cash Flow',
                     'Investing Cash Flow',
                     'Capital Expenditure',
                     'Other Investing Cash Flow',
                     'Financing Cash Flow',
                     'Net Issuance/Payments Of Debt',
                     'Net Common Stock Issuance',
                     'Cash Dividends Paid',
                     'Other Financing Cash Flow',
                     'Beginning Cash Position',
                     'Net Change in Cash',
                     'Other Changes',
                     'End Cash Position']
        }

        #INCOME STATEMENT
        def Income():
            if interval == 'annual':
                IS = firm.income_stmt
            elif interval == 'quarter':
                IS = firm.quarterly_income_stmt.iloc[:, 0:5]

                    #creating new IS line item
            IS.loc['Other Operating Expenses'] = (
                (IS.loc['Gross Profit'] if 'Gross Profit' in IS.index else np.nan)
                - (IS.loc['Research And Development'] if 'Research And Development' in IS.index else 0)
                - (IS.loc['EBITDA'] if 'EBITDA' in IS.index else 0)
            )

                    #filtering which line items to output
            IS = IS.reindex(statement_items['income'], fill_value=np.nan)

                    #renaming line item titles to better syntax
            IS.index = renamed_items['income']

            return IS
        
        #BALANCE SHEET
        def Balance():
            if interval == 'annual':
                BS = firm.balance_sheet
            elif interval == 'quarter':
                BS = firm.quarterly_balance_sheet.iloc[:, 0:5]

            BS.loc['Other Current Assets'] = (
                (BS.loc['Current Assets'] if 'Current Assets' in BS.index else np.nan)
                - (BS.loc['Cash And Cash Equivalents'] if 'Cash And Cash Equivalents' in BS.index else 0) 
                - (BS.loc['Accounts Receivable'] if 'Accounts Receivable' in BS.index else 0) 
                - (BS.loc['Inventory'] if 'Inventory' in BS.index else 0)
            )
            BS.loc['Other Non Current Assets'] = (
                (BS.loc['Total Non Current Assets'] if 'Total Non Current Assets' in BS.index else np.nan)
                - (BS.loc['Net PPE'] if 'Net PPE' in BS.index else 0)
                - (BS.loc['Goodwill And Other Intangible Assets'] if 'Goodwill And Other Intangible Assets' in BS.index else 0)
            )
            BS.loc['Other Current Liabilities'] = (
                (BS.loc['Current Liabilities'] if 'Current Liabilities' in BS.index else np.nan)
                - (BS.loc['Accounts Payable'] if 'Accounts Payable' in BS.index else 0)
                - (BS.loc['Current Debt And Capital Lease Obligation'] if 'Current Debt And Capital Lease Obligation' in BS.index else 0)
            )
            BS.loc['Other Non Current Liabilities'] = (
                (BS.loc['Total Non Current Liabilities Net Minority Interest'] if 'Total Non Current Liabilities Net Minority Interest' in BS.index else np.nan)
                - (BS.loc['Long Term Debt And Capital Lease Obligation'] if 'Long Term Debt And Capital Lease Obligation' in BS.index else 0)
            )
            BS.loc['Other Equity'] = (
                (BS.loc['Total Equity Gross Minority Interest'] if 'Total Equity Gross Minority Interest' in BS.index else np.nan)
                - (BS.loc['Retained Earnings'] if 'Retained Earnings' in BS.index else 0)
            )

            BS = BS.reindex(statement_items['balance'], fill_value=np.nan)

            BS.index = renamed_items['balance']

            return BS

        #CASH FLOW STATMENT
        def Cash():
            if interval == 'annual':
                CF = firm.cash_flow
            elif interval == 'quarter':
                CF = firm.quarterly_cash_flow.iloc[:, 0:5]

            CF.loc['Other Operating Cash Flow'] = (
                (CF.loc['Operating Cash Flow'] if 'Operating Cash Flow' in CF.index else np.nan)
                - (CF.loc['Net Income From Continuing Operations'] if 'Net Income From Continuing Operations' in CF.index else 0)
                - (CF.loc['Depreciation Amortization Depletion'] if 'Depreciation Amortization Depletion' in CF.index else 0)
                - (CF.loc['Change In Working Capital'] if 'Change In Working Capital' in CF.index else 0)
            )
            CF.loc['Other Investing Cash Flow'] = (
                (CF.loc['Investing Cash Flow'] if 'Investing Cash Flow' in CF.index else np.nan)
                - (CF.loc['Capital Expenditure'] if 'Capital Expenditure' in CF.index else 0)
            )
            CF.loc['Other Financing Cash Flow'] = (
                (CF.loc['Financing Cash Flow'] if 'Financing Cash Flow' in CF.index else np.nan)
                - (CF.loc['Net Issuance Payments Of Debt'] if 'Net Issuance Payments Of Debt' in CF.index else 0)
                - (CF.loc['Net Common Stock Issuance'] if 'Net Common Stock Issuance' in CF.index else 0)
                - (CF.loc['Cash Dividends Paid'] if 'Cash Dividends Paid' in CF.index else 0)
            )
            CF.loc['Other Changes'] = (
                (CF.loc['End Cash Position'] if 'End Cash Position' in CF.index else np.nan)
                - (CF.loc['Beginning Cash Position'] if 'Beginning Cash Position' in CF.index else 0)
                - (CF.loc['Changes In Cash'] if 'Changes In Cash' in CF.index else 0)
            )

            CF = CF.reindex(statement_items['cash'], fill_value=np.nan)

            CF.index = renamed_items['cash']

            return CF

        #STATEMENT SELECTION
        if statement == 'all':
            data = pd.concat([Income(), 
                              Balance(), 
                              Cash().loc[['Operating Cash Flow',
                                          'Change In Working Capital',
                                          'Other Operating Cash Flow',
                                          'Investing Cash Flow',
                                          'Capital Expenditure',
                                          'Other Investing Cash Flow',
                                          'Financing Cash Flow',
                                          'Net Issuance/Payments Of Debt',
                                          'Net Common Stock Issuance',
                                          'Cash Dividends Paid',
                                          'Other Financing Cash Flow',
                                          'Beginning Cash Position',
                                          'Net Change in Cash',
                                          'Other Changes',
                                          'End Cash Position']]])
        elif statement == 'income':
            data = Income()
        elif statement == 'balance':
            data = Balance()
        elif statement == 'cash':
            data = Cash()

        #UNIT SELECTION
        if unit == 'thousand':
            data /= 1000
        elif unit == 'million':
            data /= 1000000
        elif unit == 'billion':
            data /= 1000000000

        #CURRENCY SELECTION
        if currency == current_currency:
            None
        elif currency != None:
            forex_pair = f'{current_currency}/{currency}'
            url = td_baseurl + f'price?apikey={td_apikey}&symbol={forex_pair}'
            exchange_rate = requests.get(url).json()['price']
            
            data *= float(exchange_rate)
            
        #DECIMAL REMOVAL/APPROVAL
        if decimal == False:
            data = data.map(lambda x: str(x) if pd.isna(x) else x)
            data = data.map(lambda x: int('{:.0f}'.format(x)) if isinstance(x, float) else x)

        #COLUMN RENAMING
        if interval == 'annual':
            data.columns = [f'FY {str(col)[:4]}' for col in data.columns]
            data = data.iloc[:, :4]
        elif interval == 'quarter':
            data.columns = [f'{str(col)[:7]}' for col in data.columns]

        #JSON DISPLAY
        if display == 'json':
            data = data.to_dict()
        elif display == 'table':
            data = data.map(lambda x: f'{x:,}' if isinstance(x, (int, float)) and pd.notna(x) else x)

        return data
    
    def quote(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        #RAW DATA/OBSERVATIONS
        price_data = yf.download(self.ticker, progress=False)
        
        yf_quote = yf.Ticker(self.ticker).get_fast_info()

        yf_history_metadata = yf.Ticker(self.ticker).get_history_metadata()
        
        url_1 = f'{td_baseurl}quote?symbol={self.mticker}&apikey={td_apikey}'
        td_quote = requests.get(url_1).json()

        url_2 = f'{td_baseurl}price?symbol={self.mticker}&apikey={td_apikey}'
        realtime_price = float(requests.get(url_2).json()['price'])

        current_year = pd.Timestamp.now().year
        
        #QUOTE DICTIONARY FORMAT
        quote_data = {
            'symbol': td_quote.get('symbol', '-'),
            'name': td_quote.get('name', '-'),
            'exchange': td_quote.get('exchange', '-'),
            'currency': td_quote.get('currency', '-'),
            'timezone': yf_history_metadata.get('timezone','-'),
            'last trading day': {
                'date': str(price_data.index[-1].date()),
                'open': float((price_data['Open'].iloc[-1]).iloc[0]),
                'high': float((price_data['High'].iloc[-1]).iloc[0]),
                'low': float((price_data['Low'].iloc[-1]).iloc[0]),
                'close': float((price_data['Close'].iloc[-1]).iloc[0]),
                'volume': int((price_data['Volume'].iloc[-1]).iloc[0])
            },
            'ttm': {
                'high': round(float((price_data['High'].iloc[-252:].max()).iloc[0]),2),
                'low': round(float((price_data['Low'].iloc[-252:].min()).iloc[0]),2)
            },
            'percent change': {
                '5y': float(((realtime_price/price_data['Close'].iloc[-1260]) - 1).iloc[0]) if price_data.shape[0]>1260 else np.nan,
                '1y': float(((realtime_price/price_data['Close'].iloc[-252]) - 1).iloc[0]) if price_data.shape[0]>252 else np.nan,
                'ytd': float(((realtime_price/price_data['Close'][price_data.index.year == current_year].iloc[0]) - 1).iloc[0]),
                '6m': float(((realtime_price/price_data['Close'].iloc[-126]) - 1).iloc[0]) if price_data.shape[0]>126 else np.nan,
                '1m': float(((realtime_price/price_data['Close'].iloc[-21]) - 1).iloc[0]) if price_data.shape[0]>21 else np.nan,
                '5d': float(((realtime_price/price_data['Close'].iloc[-5]) - 1).iloc[0]) if price_data.shape[0]>5 else np.nan
            },
            '50d average price': float((price_data['Close'].iloc[-50:].mean()).iloc[0]),
            '200d average price': float((price_data['Close'].iloc[-200:].mean()).iloc[0]),
            '10d average volume': int((price_data['Volume'].iloc[-10:].mean()).iloc[0]),
            '90d average volume': int((price_data['Volume'].iloc[-90:].mean()).iloc[0]),
            'shares outstanding': int(yf_quote['shares']),
            'market cap': int(yf_quote.get('shares', np.nan) * realtime_price)
        }

        if display == 'json':
            return price_data.shape[0]
        elif display == 'pretty':
            print(f'''
        Identifier: {quote_data['symbol']} - {quote_data['name']}
 Exchange/Timezone: {quote_data['exchange']} - {quote_data['timezone']}
          Currency: {quote_data['currency']}
Shares Outstanding: {'{:,}'.format(quote_data['shares outstanding'])}
        Market Cap: {'{:,}'.format(quote_data['market cap'])}

{quote_data['last trading day']['date']} OHLCV------------------------
           OPEN --  {round(quote_data['last trading day']['open'],2)}
           HIGH --  {round(quote_data['last trading day']['high'],2)}
            LOW --  {round(quote_data['last trading day']['low'],2)}
          CLOSE --  {round(quote_data['last trading day']['close'],2)}
         VOLUME --  {'{:,}'.format(round(quote_data['last trading day']['volume'],2))}
TTM HIGH/LOW----------------------------
           HIGH --  {round(quote_data['ttm']['high'],2)}{'*' if price_data.shape[0]<252 else ''}
            LOW --  {round(quote_data['ttm']['low'],2)}{'*' if price_data.shape[0]<252 else ''}
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
''')

    def info(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        #RAW DATA/OBSERVATIONS
        history_metadata = yf.Ticker(self.ticker).get_history_metadata()

        info = yf.Ticker(self.ticker).get_info()

        calendar = yf.Ticker(self.ticker).get_calendar()

        headers = {'User-Agent': "ibahng21@gmail.com"}
        sec_list = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()

        url_1 = f'{td_baseurl}quote?symbol={self.mticker}&apikey={td_apikey}'
        td_quote = requests.get(url_1).json()

        #COMPANY OFFICERS
        company_officers = {}
        if 'companyOfficers' in info.keys():
            for officer in info['companyOfficers']:
                company_officers[officer['name']] = officer['title']
            
            longest_name_length = max([len(name) for name in company_officers.keys()])

        #CIK ID
        companyData = pd.DataFrame.from_dict(sec_list, orient='index')

        companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)

        try:
            index_of_ticker = int(companyData[companyData['ticker'] == self.ticker].index[0])

            cik = companyData.iloc[index_of_ticker,0]
        except IndexError:
            cik = 'No cik ID'

        info_data = {
            'symbol': td_quote.get('symbol', '-'),
            'name': td_quote.get('name', '-'),
            'exchange': td_quote.get('exchange', '-'),
            'currency': td_quote.get('currency', '-'),
            'timezone': history_metadata.get('timezone', '-'),
            'country': info.get('country', '-'),
            'industry': info.get('industry', '-'),
            'sector': info.get('sector','-'),
            'cik': cik,
            'dividend date': calendar.get('Dividend Date', '-'),
            'ex-dividend date': calendar.get('Ex-Dividend Date', '-'),
            'earnings date': calendar.get('Earnings Date', '-'),
            'website': info.get('website', '-'),
            'description': info.get('longBusinessSummary', '-'),
            'company officers': company_officers
        }

        if display == 'json':
            return info_data
        elif display == 'pretty':
            print(f'''
       Identifier: {info_data['symbol']} - {info_data['name']}
Exchange/Timezone: {info_data['exchange']} - {info_data['timezone']}
         Currency: {info_data['currency']}
          Country: {info_data['country']}
              CIK: {info_data['cik']}
  Sector/Industry: {info_data['sector']} - {info_data['industry']}
          Website: {info_data['website']}
    Earnings Date: {info_data['earnings date'][0].strftime('%B %d, %Y') if info_data['earnings date'] != '-' else '-'}
    Dividend Date: {info_data['dividend date'].strftime('%B %d, %Y') if info_data['dividend date'] != '-' else '-'}
 Ex-Dividend Date: {info_data['ex-dividend date'].strftime('%B %d, %Y') if info_data['ex-dividend date'] != '-' else '-'}

DESCRIPTION-------------------------------------------------------
{info_data['description']}

COMPANY OFFICERS--------------------------------------------------''')
        for k,v in company_officers.items():
            print(f'{k.rjust(longest_name_length)} -- {v}')

    def news(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATIONS

        news = yf.Ticker(self.ticker).get_news()

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

        if display == 'json':
            return news_data
        if display == 'pretty':
            article_strings = []
            for i in news_data:
                string = f'''{i['title']}
{i['provider']} -- {i['publish date']}

{i['snippet']}

URL: {i['url']}
---------------------------------------------------------------------------------'''
                article_strings.append(string)

            print('---------------------------------------------------------------------------------')
            for i in article_strings:
                print(i)

    def filings(self, display: str = 'json', form: str = None):
        valid_params = {'valid_display': ['json', 'pretty']}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATIONS
        headers = {'User-Agent': "ibahng21@gmail.com"}
        companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers) #requesting the cik to ticker json
        
        companyData = pd.DataFrame.from_dict(companyTickers.json(), orient='index')
        companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10) # adding leading zeros to cik

        index_of_ticker = int(companyData[companyData['ticker'] == self.ticker].index[0])

        cik = companyData.iloc[index_of_ticker,0]

        filingMetadata = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=headers)

        allForms = pd.DataFrame.from_dict(filingMetadata.json()['filings']['recent'])

        allForms = allForms[['accessionNumber','filingDate','form']]

        allForms = allForms.set_index('accessionNumber')

        if form != None:
            allForms = allForms[allForms['form'] == form]

        return allForms

    def eps_timeseries(self, interval: str = 'annual', display: str = 'json'):
        valid_params = {'valid_interval': ['quarter', 'annual'],
                        'valid_display': ['json', 'table']}
        
        params = {'interval': interval,
                  'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
        #RAW DATA/OBSERVATIONS
        url = f'https://www.alphavantage.co/query?function=EARNINGS&apikey=8SOVWDGT5EO6OB4X&symbol={self.ticker}'
        av_eps = requests.get(url).json()

        if interval == 'annual':
            annual_data = av_eps['annualEarnings']
            json_eps_data = {}
            for data_point in annual_data:
                json_eps_data[f'FY {data_point['fiscalDateEnding'][0:4]}'] = data_point['reportedEPS']
            table_eps_data = pd.DataFrame.from_dict(json_eps_data, orient='index', columns=['Reported EPS']).astype(float)
            table_eps_data = table_eps_data.map(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x)

        elif interval == 'quarter':
            quarter_data = av_eps['quarterlyEarnings']
            json_eps_data = {}
            for data_point in quarter_data:
                json_eps_data[f'{data_point['fiscalDateEnding'][0:7]}'] = {
                    'reported eps': float(data_point['reportedEPS']),
                    'estimated eps': (float(data_point['estimatedEPS']) if data_point['estimatedEPS'] != 'None' else '-'),
                    'surprise': float(data_point['surprise']),
                    'surprise percentage': (float(data_point['estimatedEPS']) if data_point['estimatedEPS'] != 'None' else '-')
                }
            table_eps_data = pd.DataFrame.from_dict(json_eps_data, orient='index')
            table_eps_data = table_eps_data.map(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x)
            table_eps_data = table_eps_data.rename(columns={'reported eps': 'Reported EPS',
                                                            'estimated eps': 'Estimated EPS',
                                                            'surprise': 'Surprise',
                                                            'surprise percentage': 'Surprise %'})
            table_eps_data = table_eps_data.iloc[::-1]

        if display == 'json':
            return json_eps_data
        elif display == 'table':
            return table_eps_data

    def analyst_estimates(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
        #RAW DATA/OBSERVATIONS

        firm = yf.Ticker(self.ticker)

        calendar = firm.get_calendar()
        earnings_estimate = firm.get_earnings_estimate()
        revenue_estimate = firm.get_revenue_estimate()
        growth_estimate = firm.get_growth_estimates()
        price_estimate = firm.get_analyst_price_targets()

        history_metadata = yf.Ticker(self.ticker).get_history_metadata()

        url_1 = f'{td_baseurl}quote?symbol={self.mticker}&apikey={td_apikey}'
        td_quote = requests.get(url_1).json()

        info = yf.Ticker(self.ticker).get_info()

        #EARNINGS
        earnings_dict = earnings_estimate.T.to_dict()
        earnings_dict['current quarter'] = earnings_dict.pop('0q')
        earnings_dict['next quarter'] = earnings_dict.pop('+1q')
        earnings_dict['current year'] = earnings_dict.pop('0y')
        earnings_dict['next year'] = earnings_dict.pop('+1y')
        

        #REVENUE
        revenue_dict = revenue_estimate.T.to_dict()
        revenue_dict['current quarter'] = revenue_dict.pop('0q')
        revenue_dict['next quarter'] = revenue_dict.pop('+1q')
        revenue_dict['current year'] = revenue_dict.pop('0y')
        revenue_dict['next year'] = revenue_dict.pop('+1y')

        #GROWTH
        growth_dict = growth_estimate.T.to_dict()
        for k in growth_dict.keys():
            del growth_dict[k]['industry']
            del growth_dict[k]['sector']

        growth_dict['current quarter'] = growth_dict.pop('0q')
        growth_dict['next quarter'] = growth_dict.pop('+1q')
        growth_dict['current year'] = growth_dict.pop('0y')
        growth_dict['next year'] = growth_dict.pop('+1y')

        #PRICE
        price_dict = price_estimate

        estimate_data = {
            'symbol': td_quote['symbol'],
            'name': td_quote['name'],
            'exchange': td_quote['exchange'],
            'currency': td_quote['currency'],
            'timezone': history_metadata['timezone'],
            'earnings date': calendar['Earnings Date'],
            'dividend date': (calendar['Dividend Date'] if 'Dividend Date' in calendar.keys() else '-'),
            'ex-dividend date': (calendar['Ex-Dividend Date'] if 'Ex-Dividend Date' in calendar.keys() else '-'),
            'earnings_estimate': earnings_dict,
            'revenue_estimate': revenue_dict,
            'growth_estimate': growth_dict,
            'price_estimate': price_dict,
        }

        if display == 'json':
            return estimate_data
        elif display == 'pretty':
            def two(num):
                return '{:.2f}'.format(num)
            
            def com(num):
                return '{:,}'.format(num)

            e = estimate_data['earnings_estimate']
            r = estimate_data['revenue_estimate']
            g = estimate_data['growth_estimate']

            return f'''
       Identifier: {estimate_data['symbol']} - {estimate_data['name']}
Exchange/Timezone: {estimate_data['exchange']} - {estimate_data['timezone']}
         Currency: {estimate_data['currency']}
    Earnings Date: {estimate_data['earnings date'][0].strftime('%B %d, %Y')}
    Dividend Date: {estimate_data['dividend date'].strftime('%B %d, %Y') if estimate_data['dividend date'] != '-' else '-'}
 Ex-Dividend Date: {estimate_data['ex-dividend date'].strftime('%B %d, %Y') if estimate_data['ex-dividend date'] != '-' else '-'}

EARNINGS ESTIMATE-------------------------------------------------------
                 Current |    Next | Current |    Next |
                 Quarter | Quarter |    Year |    Year |
          HIGH  {str(two(e['current quarter']['high'])).rjust(8)} |{str(two(e['next quarter']['high'])).rjust(8)} |{str(two(e['current year']['high'])).rjust(8)} |{str(two(e['next year']['high'])).rjust(8)} |
       AVERAGE  {str(two(e['current quarter']['avg'])).rjust(8)} |{str(two(e['next quarter']['avg'])).rjust(8)} |{str(two(e['current year']['avg'])).rjust(8)} |{str(two(e['next year']['avg'])).rjust(8)} |
           LOW  {str(two(e['current quarter']['low'])).rjust(8)} |{str(two(e['next quarter']['low'])).rjust(8)} |{str(two(e['current year']['low'])).rjust(8)} |{str(two(e['next year']['low'])).rjust(8)} |
       -1Y EPS  {str(two(e['current quarter']['yearAgoEps'])).rjust(8)} |{str(two(e['next quarter']['yearAgoEps'])).rjust(8)} |{str(two(e['current year']['yearAgoEps'])).rjust(8)} |{str(two(e['next year']['yearAgoEps'])).rjust(8)} |
      % CHANGE  {str(two(e['current quarter']['growth']*100)).rjust(8)}%|{str(two(e['next quarter']['growth']*100)).rjust(8)}%|{str(two(e['current year']['growth']*100)).rjust(8)}%|{str(two(e['next year']['growth']*100)).rjust(8)}%|
 # OF ANALYSTS  {str(int(e['current quarter']['numberOfAnalysts'])).rjust(8)} |{str(int(e['next quarter']['numberOfAnalysts'])).rjust(8)} |{str(int(e['current year']['numberOfAnalysts'])).rjust(8)} |{str(int(e['next year']['numberOfAnalysts'])).rjust(8)} |

REVENUE ESTIMATE-----------------------------------------in {info['financialCurrency'].rjust(3)} millions
                 Current |    Next | Current |    Next |
                 Quarter | Quarter |    Year |    Year |
          HIGH  {com(int(r['current quarter']['high']/1000000)).rjust(8)} |{com(int(r['next quarter']['high']/1000000)).rjust(8)} |{com(int(r['current year']['high']/1000000)).rjust(8)} |{com(int(r['next year']['high']/1000000)).rjust(8)} |
       AVERAGE  {com(int(r['current quarter']['avg']/1000000)).rjust(8)} |{com(int(r['next quarter']['avg']/1000000)).rjust(8)} |{com(int(r['current year']['avg']/1000000)).rjust(8)} |{com(int(r['next year']['avg']/1000000)).rjust(8)} |
           LOW  {com(int(r['current quarter']['low']/1000000)).rjust(8)} |{com(int(r['next quarter']['low']/1000000)).rjust(8)} |{com(int(r['current year']['low']/1000000)).rjust(8)} |{com(int(r['next year']['low']/1000000)).rjust(8)} |
       -1Y EPS  {com(int(r['current quarter']['yearAgoRevenue']/1000000)).rjust(8)} |{com(int(r['next quarter']['yearAgoRevenue']/1000000)).rjust(8)} |{com(int(r['current year']['yearAgoRevenue']/1000000)).rjust(8)} |{com(int(r['next year']['yearAgoRevenue']/1000000)).rjust(8)} |
      % CHANGE  {str(two(r['current quarter']['growth']*100)).rjust(8)}%|{str(two(r['next quarter']['growth']*100)).rjust(8)}%|{str(two(r['current year']['growth']*100)).rjust(8)}%|{str(two(r['next year']['growth']*100)).rjust(8)}%|
 # OF ANALYSTS  {str(int(r['current quarter']['numberOfAnalysts'])).rjust(8)} |{str(int(r['next quarter']['numberOfAnalysts'])).rjust(8)} |{str(int(r['current year']['numberOfAnalysts'])).rjust(8)} |{str(int(r['next year']['numberOfAnalysts'])).rjust(8)} |

GROWTH ESTIMATE---------------------------------------------------------
                 Current |    Next | Current |    Next |
                 Quarter | Quarter |    Year |    Year |
% STOCK CHANGE  {str(two(g['current quarter']['stock']*100)).rjust(7)}% |{str(two(g['next quarter']['stock']*100)).rjust(7)}% |{str(two(g['current year']['stock']*100)).rjust(7)}% |{str(two(g['next year']['stock']*100)).rjust(7)}% |
% INDEX CHANGE  {str(two(g['current quarter']['index']*100)).rjust(7)}% |{str(two(g['next quarter']['index']*100)).rjust(7)}% |{str(two(g['current year']['index']*100)).rjust(7)}% |{str(two(g['next year']['index']*100)).rjust(7)}% |

PRICE ESTIMATE----------------------------------------------------------
       CURRENT -- {two(estimate_data['price_estimate']['current'])}
        MEDIAN -- {two(estimate_data['price_estimate']['median'])}
          HIGH -- {two(estimate_data['price_estimate']['high'])}
          MEAN -- {two(estimate_data['price_estimate']['mean'])}
           LOW -- {two(estimate_data['price_estimate']['low'])}'''

    def dividend(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'table'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
    
        #RAW DATA/OBSERVATIONS
        dividends = yf.Ticker(self.ticker).get_dividends()

        renamed_dates = {}
        for i in dividends.keys():
            renamed_dates[i] = str(i)[0:10]

        #renaming the datetime indexes to date
        dividends = dividends.rename(renamed_dates)

        #converting series to dict
        dividends_dict = dividends.to_dict()

        #converting dict to dataframe
        dividends_df = pd.DataFrame.from_dict(dividends_dict, orient='index', columns=['Dividends'])

        #making all values two decimal points
        dividends_df = dividends_df.map(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x)

        if display == 'json':
            return dividends_dict
        elif display == 'table':
            return dividends_df

    def split(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'table'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
        #RAW DATA/OBSERVATIONS
        splits = yf.Ticker(self.ticker).get_splits()

        renamed_dates = {}
        for i in splits.keys():
            renamed_dates[i] = str(i)[0:10]

        splits = splits.rename(renamed_dates)

        splits_dict = splits.to_dict()

        splits_df = pd.DataFrame.from_dict(splits_dict, orient='index', columns=['Splits'])

        if display == 'json':
            return splits_dict
        elif display == 'table':
            return splits_df

    def stats(self, display: str = 'json'):
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATIONS
        stmt_df = self.statement(display='table', unit='million')
        stmt_df = stmt_df.map(lambda x: pd.to_numeric(x.replace(',', ''), errors='coerce') if isinstance(x, str) else x)
        stmt_loc = stmt_df.loc

        raw_IS = yf.Ticker(self.ticker).income_stmt

        q_stmt_df = self.statement(display='table', unit='million', interval='quarter')
        q_stmt_df = q_stmt_df.map(lambda x: pd.to_numeric(x.replace(',', ''), errors='coerce') if isinstance(x, str) else x)

        raw_qIS = yf.Ticker(self.ticker).quarterly_income_stmt

        url = f'{td_baseurl}price?symbol={self.mticker}&apikey={td_apikey}'
        realtime_price = float(requests.get(url).json()['price'])

        yf_quote = yf.Ticker(self.ticker).get_fast_info()
        
        url_1 = f'{td_baseurl}quote?symbol={self.mticker}&apikey={td_apikey}'
        td_quote = requests.get(url_1).json()

        history_metadata = yf.Ticker(self.ticker).get_history_metadata()

        #SAFE EVAL - a exception handling function
        #def safe_eval(expression, default_value = float('nan')):
            #try:
                #result = expression
                #return result
            #except Exception:
                #return default_value

        #PROFITABILITY
        stmt_loc['gross margin'] = stmt_loc['Gross Profit']/stmt_loc['Total Revenue']
        stmt_loc['ebit margin'] = stmt_loc['EBIT']/stmt_loc['Total Revenue']
        stmt_loc['net margin'] = stmt_loc['Net Income']/stmt_loc['Total Revenue']
        stmt_loc['roa'] = stmt_loc['Net Income']/stmt_loc['Total Assets']
        stmt_loc['roe'] = stmt_loc['Net Income']/stmt_loc['Total Equity']

        #LIQUIDITY
        stmt_loc['current ratio'] = stmt_loc['Total Current Assets']/stmt_loc['Total Current Liabilities']
        stmt_loc['quick ratio'] = (stmt_loc['Total Current Assets'] - stmt_loc['Inventory'])/stmt_loc['Total Current Liabilities']
        stmt_loc['cash ratio'] = stmt_loc['Cash And Cash Equivalents']/stmt_loc['Total Current Liabilities']

        #LEVERAGE
        stmt_loc['debt to equity'] = stmt_loc['Total Liabilities']/stmt_loc['Total Equity']
        stmt_loc['debt to assets'] = stmt_loc['Total Liabilities']/stmt_loc['Total Assets']
        stmt_loc['interest coverage ratio'] = stmt_loc['EBIT']/stmt_loc['Interest Expense']

        #EFFICIENCY
        stmt_loc['inventory turnover'] = stmt_loc['Cost Of Revenue'] / ((stmt_loc['Inventory'] + stmt_df.shift(-1, axis=1).loc['Inventory'])/2)
        stmt_loc['receivables turnover'] = stmt_loc['Total Revenue'] / ((stmt_loc['Accounts Receivable'] + stmt_df.shift(-1, axis=1).loc['Accounts Receivable'])/2)
        stmt_loc['payables turnover'] = stmt_loc['Cost Of Revenue'] / ((stmt_loc['Accounts Payable'] + stmt_df.shift(-1, axis=1).loc['Accounts Payable'])/2)
        stmt_loc['dio'] = 365 / stmt_loc['inventory turnover']
        stmt_loc['dso'] = 365 / stmt_loc['receivables turnover']
        stmt_loc['dpo'] = 365 / stmt_loc['payables turnover']
        stmt_loc['cash conversion cycle'] = stmt_loc['dso'] + stmt_loc['dio'] - stmt_loc['dpo']

        #CASH FLOW
        stmt_loc['fcff_DA.WC'] = stmt_loc['EBIT'] * (1 - (stmt_loc['Tax Provision']/stmt_loc['Pretax Income'])) + stmt_loc['Depreciation and Amortization'] + stmt_loc['Change In Working Capital'] + stmt_loc['Capital Expenditure']
        stmt_loc['fcff_DA.WC.otherNonCash'] = stmt_loc['fcff_DA.WC'] + stmt_loc['Other Operating Cash Flow']
        stmt_loc['fcfe_DA.WC'] = stmt_loc['Net Income'] + stmt_loc['Depreciation and Amortization'] + stmt_loc['Change In Working Capital'] + stmt_loc['Capital Expenditure'] + stmt_loc['Net Issuance/Payments Of Debt']
        stmt_loc['fcfe_DA.WC.otherNonCash'] = stmt_loc['Operating Cash Flow'] + stmt_loc['Capital Expenditure'] + stmt_loc['Net Issuance/Payments Of Debt']

        #GROWTH
        stmt_loc['revenue growth rate'] = (stmt_loc['Total Revenue'] / stmt_df.shift(-1, axis=1).loc['Total Revenue']) - 1
        stmt_loc['EBIT growth rate'] = (stmt_loc['EBIT'] / stmt_df.shift(-1, axis=1).loc['EBIT']) - 1

        #VALUATION (TIMESERIES)
        #------------------FY END DATE STOCK PRICES
        date_lists = []
        for i in raw_IS.columns[0:4]:
            a = []
            a.append(str(i.date()))
            a.append(str(i.date() + timedelta(days=-1)))
            a.append(str(i.date() + timedelta(days=-2)))
            a.append(str(i.date() + timedelta(days=-3)))
            a.append(str(i.date() + timedelta(days=-4)))
            a.append(str(i.date() + timedelta(days=-5)))
            date_lists.append(a)

        FY_prices = []
        for date_list in date_lists:
            for date in date_list:
                try:
                    a = yf.download(self.ticker, progress=False, ignore_tz=True).loc[date]
                    FY_prices.append(float(a.iloc[0]))
                    break
                except KeyError:
                    None

        if len(FY_prices) == len(raw_IS.columns[0:4]):
            for i in range(len(raw_IS.columns[0:4]) - len(FY_prices)):
                FY_prices.append(np.nan)

        #FY END DATE VALUATION STATS
        stmt_loc['stock price'] = FY_prices
        stmt_loc['shares outstanding'] = raw_IS.loc['Basic Average Shares'].tolist()[0:4]
        stmt_loc['market cap'] = (stmt_loc['stock price'] * stmt_loc['shares outstanding'])/1000000

        stmt_loc['pe'] = stmt_loc['market cap'] / stmt_loc['Net Income']
        stmt_loc['ps'] = stmt_loc['market cap'] / stmt_loc['Total Revenue']
        stmt_loc['pb'] = stmt_loc['market cap'] / stmt_loc['Total Equity']
        stmt_loc['eps'] = raw_IS.loc['Basic EPS'].tolist()[0:4]
        stmt_loc['dividend yield'] = -stmt_loc['Cash Dividends Paid'] / stmt_loc['market cap']
        stmt_loc['dividend payout ratio'] = -stmt_loc['Cash Dividends Paid'] / stmt_loc['Net Income']
        stmt_loc['enterprise value'] = stmt_loc['market cap'] + stmt_loc['Total Liabilities'] - stmt_loc['Cash And Cash Equivalents']
            #MARKET CAP IS ABOVE
        stmt_loc['ev/ebitda'] = stmt_loc['enterprise value'] / stmt_loc['EBITDA']
        stmt_loc['ev/ebit'] = stmt_loc['enterprise value'] / stmt_loc['EBIT']

#RECENT FIGURES-------------------------------

        #RECENT FIGURES - VALUTION
        market_cap = int(yf_quote['shares'] * realtime_price)/1000000
        
        try:
            ttm_pe = market_cap / sum(q_stmt_df.loc['Net Income'].tolist()[0:4])
        except ZeroDivisionError:
            ttm_pe = float('inf')

        try:
            ttm_ps = market_cap / sum(q_stmt_df.loc['Total Revenue'].tolist()[0:4])
        except ZeroDivisionError:
            ttm_ps = float('inf')

        
        mrq_pb = market_cap / q_stmt_df.iloc[:,0].loc['Total Equity']
        mrq_eps = raw_qIS.iloc[:,0].loc['Basic EPS']
        ttm_eps = sum(raw_qIS.loc['Basic EPS'].tolist()[0:4])
        ttm_dividend_yield = -sum(q_stmt_df.loc['Cash Dividends Paid'].tolist()[0:4]) / market_cap

        try:
            mrq_dividend_payout_ratio = -q_stmt_df.iloc[:,0].loc['Cash Dividends Paid'] / q_stmt_df.iloc[:,0].loc['Net Income']
        except ZeroDivisionError:
            mrq_dividend_payout_ratio = np.nan
        
        try:
            ttm_dividend_payout_ratio = -sum(q_stmt_df.loc['Cash Dividends Paid'].tolist()[0:4]) / sum(q_stmt_df.loc['Net Income'].tolist()[0:4])
        except ZeroDivisionError:
            ttm_dividend_payout_ratio = np.nan
        
        mrq_enterprise_value = market_cap + q_stmt_df.iloc[:,0].loc['Total Liabilities'] - q_stmt_df.iloc[:,0].loc['Cash And Cash Equivalents']
        
        try:
            ttm_ev_ebitda = mrq_enterprise_value / sum(q_stmt_df.loc['EBITDA'].tolist()[0:4])
        except ZeroDivisionError:
            ttm_ev_ebitda = np.nan
        
        try:
            ttm_ev_ebit = mrq_enterprise_value / sum(q_stmt_df.loc['EBIT'].tolist()[0:4])
        except ZeroDivisionError:
            ttm_ev_ebit = np.nan

        #RECENT FIGURES - PROFITABILITY
        try:
            mrq_gross_margin = q_stmt_df.iloc[:,0].loc['Gross Profit'] / q_stmt_df.iloc[:,0].loc['Total Revenue']
        except ZeroDivisionError:
            mrq_gross_margin = np.nan

        try:
            mrq_ebit_margin = q_stmt_df.iloc[:,0].loc['EBIT'] / q_stmt_df.iloc[:,0].loc['Total Revenue']
        except ZeroDivisionError:
            mrq_ebit_margin 

        try:
            mrq_net_margin = q_stmt_df.iloc[:,0].loc['Net Income'] / q_stmt_df.iloc[:,0].loc['Total Revenue']
        except ZeroDivisionError:
            mrq_net_margin = np.nan
        
        ttm_roa = sum(q_stmt_df.loc['Net Income'].tolist()[0:4]) / q_stmt_df.iloc[:,0].loc['Total Assets']
        ttm_roe = sum(q_stmt_df.loc['Net Income'].tolist()[0:4]) / q_stmt_df.iloc[:,0].loc['Total Equity']

        #RECENT FIGURES - GROWTH
        try:
            mrq_revenue_growth = (q_stmt_df.loc['Total Revenue'].tolist()[0]/q_stmt_df.loc['Total Revenue'].tolist()[1]) - 1
        except ZeroDivisionError:
            mrq_revenue_growth = np.nan

        try:
            mrq_ebit_growth = (q_stmt_df.loc['EBIT'].tolist()[0]/q_stmt_df.loc['EBIT'].tolist()[1]) - 1
        except ZeroDivisionError:
            mrq_ebit_growth = np.nan

        #RECENT FIGURES - LIQUIDITY
        try:
            mrq_current_ratio = q_stmt_df.iloc[:,0].loc['Total Current Assets'] / q_stmt_df.iloc[:,0].loc['Total Current Liabilities']
        except ZeroDivisionError:
            mrq_current_ratio = np.nan

        try:
            mrq_quick_ratio = (q_stmt_df.iloc[:,0].loc['Total Current Assets'] - q_stmt_df.iloc[:,0].loc['Inventory']) / q_stmt_df.iloc[:,0].loc['Total Current Liabilities']
        except ZeroDivisionError:
            mrq_quick_ratio = np.nan

        try:
            mrq_cash_ratio = q_stmt_df.iloc[:,0].loc['Cash And Cash Equivalents'] / q_stmt_df.iloc[:,0].loc['Total Current Liabilities']
        except ZeroDivisionError:
            mrq_cash_ratio = np.nan


        #RECENT FIGURES - LEVERAGE
        mrq_debt_to_equity = q_stmt_df.iloc[:,0].loc['Total Liabilities'] / q_stmt_df.iloc[:,0].loc['Total Equity']
        mrq_debt_to_assets = q_stmt_df.iloc[:,0].loc['Total Liabilities'] / q_stmt_df.iloc[:,0].loc['Total Assets']
        mrq_interst_coverage_ratio = q_stmt_df.iloc[:,0].loc['EBIT'] / q_stmt_df.iloc[:,0].loc['Interest Expense']

        #RECENT FIGURES - EFFICIENCY
        try:
            ttm_inventory_turnover = sum(q_stmt_df.loc['Cost Of Revenue'].tolist()[0:4]) / ((q_stmt_df.loc['Inventory'].tolist()[0] + q_stmt_df.loc['Inventory'].tolist()[3])/2)
        except ZeroDivisionError:
            ttm_inventory_turnover = np.nan
        
        try:
            ttm_receivables_turnover = sum(q_stmt_df.loc['Total Revenue'].tolist()[0:4]) / ((q_stmt_df.loc['Accounts Receivable'].tolist()[0]+q_stmt_df.loc['Accounts Receivable'].tolist()[3])/2)
        except ZeroDivisionError:
            ttm_receivables_turnover = np.nan
            
        try:
            ttm_payables_turnover = sum(q_stmt_df.loc['Cost Of Revenue'].tolist()[0:4]) / ((q_stmt_df.loc['Accounts Payable'].tolist()[0]+q_stmt_df.loc['Accounts Payable'].tolist()[3])/2)
        except ZeroDivisionError:
            ttm_payables_turnover = np.nan
        ttm_dio = 365 / ttm_inventory_turnover
        ttm_dso = 365 / ttm_receivables_turnover
        ttm_dpo = 365 / ttm_payables_turnover
        ttm_cash_conversion_cycle = ttm_dso + ttm_dio - ttm_dpo

        #RECENT FIGURES - CASHFLOW
        ttm_fcff_DA_WC = sum(q_stmt_df.loc['EBIT'].tolist()[0:4]) * (1 - sum(q_stmt_df.loc['Tax Provision'].tolist()[0:4])/sum(q_stmt_df.loc['Pretax Income'].tolist()[0:4])) + sum(q_stmt_df.loc['Depreciation and Amortization'].tolist()[0:4]) + sum(q_stmt_df.loc['Change In Working Capital'].tolist()[0:4]) + sum(q_stmt_df.loc['Capital Expenditure'].tolist()[0:4])
        ttm_fcff_DA_WC_nonCash = ttm_fcff_DA_WC + sum(q_stmt_df.loc['Other Operating Cash Flow'].tolist()[0:4])
        ttm_fcfe_DA_WC = sum(q_stmt_df.loc['Net Income'].tolist()[0:4]) + sum(q_stmt_df.loc['Depreciation and Amortization'].tolist()[0:4]) + sum(q_stmt_df.loc['Change In Working Capital'].tolist()[0:4]) + sum(q_stmt_df.loc['Capital Expenditure'].tolist()[0:4]) + sum(q_stmt_df.loc['Net Issuance/Payments Of Debt'].tolist()[0:4])
        ttm_fcfe_DA_WC_nonCash = sum(q_stmt_df.loc['Operating Cash Flow'].tolist()[0:4]) + sum(q_stmt_df.loc['Capital Expenditure'].tolist()[0:4]) + sum(q_stmt_df.loc['Net Issuance/Payments Of Debt'].tolist()[0:4])


        base_data = {
            'symbol': td_quote['symbol'],
            'name': td_quote['name'],
            'exchange': td_quote['exchange'],
            'currency': td_quote['currency'],
            'timezone': history_metadata['timezone'],
        }

        stats_data = {
            'profitability': {
                'gross margin': stmt_loc['gross margin'].to_dict(),
                'ebit margin': stmt_loc['ebit margin'].to_dict(),
                'net margin': stmt_loc['net margin'].to_dict(),
                'roa': stmt_loc['roa'].to_dict(),
                'roe': stmt_loc['roe'].to_dict()
            },
            'liquidity': {
                'current ratio': stmt_loc['current ratio'].to_dict(),
                'quick ratio': stmt_loc['quick ratio'].to_dict(),
                'cash ratio': stmt_loc['cash ratio'].to_dict()
            },
            'leverage': {
                'debt to equity': stmt_loc['debt to equity'].to_dict(),
                'debt to assets': stmt_loc['debt to assets'].to_dict(),
                'interest coverage ratio': stmt_loc['interest coverage ratio'].to_dict()
            },
            'efficiency': {
                'inventory turnover': stmt_loc['inventory turnover'].to_dict(),
                'receivables turnover': stmt_loc['receivables turnover'].to_dict(),
                'payables turnover': stmt_loc['payables turnover'].to_dict(),
                'dio': stmt_loc['dio'].to_dict(),
                'dso': stmt_loc['dso'].to_dict(),
                'dpo': stmt_loc['dpo'].to_dict(),
                'cash conversion cycle': stmt_loc['cash conversion cycle'].to_dict()
            },
            'valuation': {
                'pe': stmt_loc['pe'].to_dict(),
                'ps': stmt_loc['ps'].to_dict(),
                'pb': stmt_loc['pb'].to_dict(),
                'eps': stmt_loc['eps'].to_dict(),
                'dividend yield': stmt_loc['dividend yield'].to_dict(),
                'dividend payout ratio': stmt_loc['dividend payout ratio'].to_dict(),
                'enterprise value': stmt_loc['enterprise value'].to_dict(),
                'market cap': stmt_loc['market cap'].to_dict(),
                'ev/ebitda': stmt_loc['ev/ebitda'].to_dict(),
                'ev/ebit': stmt_loc['ev/ebit'].to_dict()
            },
            'cash flow': {
                'fcff_DA.WC': stmt_loc['fcff_DA.WC'].to_dict(),
                'fcff_DA.WC.otherNonCash': stmt_loc['fcff_DA.WC.otherNonCash'].to_dict(),
                'fcfe_DA.WC': stmt_loc['fcfe_DA.WC'].to_dict(),
                'fcfe_DA.WC.otherNonCash': stmt_loc['fcfe_DA.WC.otherNonCash'].to_dict()
            },
            'growth': {
                'revenue growth rate': stmt_loc['revenue growth rate'].to_dict(),
                'ebit growth rate': stmt_loc['EBIT growth rate'].to_dict()
            }
        }

        p_key = stats_data['profitability']
        li_key = stats_data['liquidity']
        le_key = stats_data['leverage']
        e_key = stats_data['efficiency']
        v_key = stats_data['valuation']
        cf_key = stats_data['cash flow']
        g_key = stats_data['growth']
        
        #ADDING ALL MRQ/TTM/NOW FIFGURES
        #Profitability
        p_key['gross margin']['mrq'] = mrq_gross_margin
        p_key['ebit margin']['mrq'] = mrq_ebit_margin
        p_key['net margin']['mrq'] = mrq_net_margin
        p_key['roa']['ttm'] = ttm_roa
        p_key['roe']['ttm'] = ttm_roe
        
        #Liquidity
        li_key['current ratio']['mrq'] = mrq_current_ratio
        li_key['quick ratio']['mrq'] = mrq_quick_ratio
        li_key['cash ratio']['mrq'] = mrq_cash_ratio

        #Leverage
        le_key['debt to equity']['mrq'] = mrq_debt_to_equity
        le_key['debt to assets']['mrq'] = mrq_debt_to_assets
        le_key['interest coverage ratio']['mrq'] = mrq_interst_coverage_ratio

        #Efficiency
        e_key['inventory turnover']['ttm'] = ttm_inventory_turnover
        e_key['receivables turnover']['ttm'] = ttm_receivables_turnover
        e_key['payables turnover']['ttm'] = ttm_payables_turnover
        e_key['dio']['ttm'] = ttm_dio
        e_key['dso']['ttm'] = ttm_dso
        e_key['dpo']['ttm'] = ttm_dpo
        e_key['cash conversion cycle']['ttm'] = ttm_cash_conversion_cycle

        #Valuation
        v_key['pe']['ttm'] = ttm_pe
        v_key['ps']['ttm'] = ttm_ps
        v_key['pb']['mrq'] = mrq_pb
        v_key['eps']['mrq'] = mrq_eps
        v_key['eps']['ttm'] = ttm_eps
        v_key['dividend yield']['ttm'] = ttm_dividend_yield
        v_key['dividend payout ratio']['mrq'] = mrq_dividend_payout_ratio
        v_key['dividend payout ratio']['ttm'] = ttm_dividend_payout_ratio
        v_key['enterprise value']['mrq'] = mrq_enterprise_value
        v_key['market cap']['now'] = market_cap
        v_key['ev/ebitda']['ttm'] = ttm_ev_ebitda
        v_key['ev/ebit']['ttm'] = ttm_ev_ebit

        #Cash Flow
        cf_key['fcff_DA.WC']['ttm'] = ttm_fcff_DA_WC
        cf_key['fcff_DA.WC.otherNonCash']['ttm'] = ttm_fcff_DA_WC_nonCash
        cf_key['fcfe_DA.WC']['ttm'] = ttm_fcfe_DA_WC
        cf_key['fcfe_DA.WC.otherNonCash']['ttm'] = ttm_fcfe_DA_WC_nonCash

        #Growth
        g_key['revenue growth rate']['mrq'] = mrq_revenue_growth
        g_key['ebit growth rate']['mrq'] = mrq_ebit_growth

        if display == 'json':
            return FY_prices
        if display == 'pretty':
            def trj(num):
                return '{:.2f}'.format(num).rjust(10)
           
            def icrj(num):
                if math.isnan(num) == True:
                    return '       nan'
                else:
                    return '{:,}'.format(int(num)).rjust(10)
            
            p = stats_data['profitability']
            g = stats_data['growth']
            li = stats_data['liquidity']
            le = stats_data['leverage']
            e = stats_data['efficiency']
            cf = stats_data['cash flow']
            v = stats_data['valuation']

            fy = stmt_df.columns.to_list()

            print(f'''
       Identifier: {base_data['symbol']} - {base_data['name']}
Exchange/Timezone: {base_data['exchange']} - {base_data['timezone']}
         Currency: {base_data['currency']}

                                 LATEST |   {stmt_df.columns[0]} |   {stmt_df.columns[1]} |   {stmt_df.columns[2]} |   {stmt_df.columns[3]} |
VALUATION--------------------------------------------------------------------------------
                   P/E  ttm  {trj(v['pe']['ttm'])} |{trj(v['pe'][fy[0]])} |{trj(v['pe'][fy[1]])} |{trj(v['pe'][fy[2]])} |{trj(v['pe'][fy[3]])} |
                   P/S  ttm  {trj(v['ps']['ttm'])} |{trj(v['ps'][fy[0]])} |{trj(v['ps'][fy[1]])} |{trj(v['ps'][fy[2]])} |{trj(v['ps'][fy[3]])} |
                   P/B  mrq  {trj(v['pb']['mrq'])} |{trj(v['pb'][fy[0]])} |{trj(v['pb'][fy[1]])} |{trj(v['pb'][fy[2]])} |{trj(v['pb'][fy[3]])} |
                   EPS  ttm  {trj(v['eps']['ttm'])} |{trj(v['eps'][fy[0]])} |{trj(v['eps'][fy[1]])} |{trj(v['eps'][fy[2]])} |{trj(v['eps'][fy[3]])} |
        DIVIDEND YIELD  ttm  {trj(v['dividend yield']['ttm']*100)}%|{trj(v['dividend yield'][fy[0]]*100)}%|{trj(v['dividend yield'][fy[1]]*100)}%|{trj(v['dividend yield'][fy[2]]*100)}%|{trj(v['dividend yield'][fy[3]]*100)}%|
 DIVIDEND PAYOUT RATIO  ttm  {trj(v['dividend payout ratio']['ttm']*100)}%|{trj(v['dividend payout ratio'][fy[0]]*100)}%|{trj(v['dividend payout ratio'][fy[1]]*100)}%|{trj(v['dividend payout ratio'][fy[2]]*100)}%|{trj(v['dividend payout ratio'][fy[3]]*100)}%|
      ENTERPRISE VALUE  mrq  {icrj(v['enterprise value']['mrq'])} |{icrj(v['enterprise value'][fy[0]])} |{icrj(v['enterprise value'][fy[1]])} |{icrj(v['enterprise value'][fy[2]])} |{icrj(v['enterprise value'][fy[3]])} |
            MARKET CAP  now  {icrj(v['market cap']['now'])} |{icrj(v['market cap'][fy[0]])} |{icrj(v['market cap'][fy[1]])} |{icrj(v['market cap'][fy[2]])} |{icrj(v['market cap'][fy[3]])} |
             EV/EBITDA  ttm  {trj(v['ev/ebitda']['ttm'])} |{trj(v['ev/ebitda'][fy[0]])} |{trj(v['ev/ebitda'][fy[1]])} |{trj(v['ev/ebitda'][fy[2]])} |{trj(v['ev/ebitda'][fy[3]])} |
               EV/EBIT  ttm  {trj(v['ev/ebit']['ttm'])} |{trj(v['ev/ebit'][fy[0]])} |{trj(v['ev/ebit'][fy[1]])} |{trj(v['ev/ebit'][fy[2]])} |{trj(v['ev/ebit'][fy[3]])} |
                            
PROFITABILITY----------------------------------------------------------------------------
          GROSS MARGIN  mrq  {trj(p['gross margin']['mrq']*100)}%|{trj(p['gross margin'][fy[0]]*100)}%|{trj(p['gross margin'][fy[1]]*100)}%|{trj(p['gross margin'][fy[2]]*100)}%|{trj(p['gross margin'][fy[3]]*100)}%|
           EBIT MARGIN  mrq  {trj(p['ebit margin']['mrq']*100)}%|{trj(p['ebit margin'][fy[0]]*100)}%|{trj(p['ebit margin'][fy[1]]*100)}%|{trj(p['ebit margin'][fy[2]]*100)}%|{trj(p['ebit margin'][fy[3]]*100)}%|
            NET MARGIN  mrq  {trj(p['net margin']['mrq']*100)}%|{trj(p['net margin'][fy[0]]*100)}%|{trj(p['net margin'][fy[1]]*100)}%|{trj(p['net margin'][fy[2]]*100)}%|{trj(p['net margin'][fy[3]]*100)}%|
                   ROA  ttm  {trj(p['roa']['ttm']*100)}%|{trj(p['roa'][fy[0]]*100)}%|{trj(p['roa'][fy[1]]*100)}%|{trj(p['roa'][fy[2]]*100)} |{trj(p['roa'][fy[3]]*100)}%|
                   ROE  ttm  {trj(p['roe']['ttm']*100)}%|{trj(p['roe'][fy[0]]*100)}%|{trj(p['roe'][fy[1]]*100)}%|{trj(p['roe'][fy[2]]*100)} |{trj(p['roe'][fy[3]]*100)}%|

GROWTH-----------------------------------------------------------------------------------
   REVENUE GROWTH RATE  mrq  {trj(g['revenue growth rate']['mrq']*100)}%|{trj(g['revenue growth rate'][fy[0]]*100)}%|{trj(g['revenue growth rate'][fy[1]]*100)}%|{trj(g['revenue growth rate'][fy[2]]*100)}%|{'-'.rjust(10)} |
      EBIT GROWTH RATE  mrq  {trj(g['ebit growth rate']['mrq']*100)}%|{trj(g['ebit growth rate'][fy[0]]*100)}%|{trj(g['ebit growth rate'][fy[1]]*100)}%|{trj(g['ebit growth rate'][fy[2]]*100)}%|{'-'.rjust(10)} |

LIQUIDITY--------------------------------------------------------------------------------
         CURRENT RATIO  mrq  {trj(li['current ratio']['mrq'])} |{trj(li['current ratio'][fy[0]])} |{trj(li['current ratio'][fy[1]])} |{trj(li['current ratio'][fy[2]])} |{trj(li['current ratio'][fy[3]])} |
           QUICK RATIO  mrq  {trj(li['quick ratio']['mrq'])} |{trj(li['quick ratio'][fy[0]])} |{trj(li['quick ratio'][fy[1]])} |{trj(li['quick ratio'][fy[2]])} |{trj(li['quick ratio'][fy[3]])} |
            CASH RATIO  mrq  {trj(li['cash ratio']['mrq'])} |{trj(li['cash ratio'][fy[0]])} |{trj(li['cash ratio'][fy[1]])} |{trj(li['cash ratio'][fy[2]])} |{trj(li['cash ratio'][fy[3]])} |

LEVERAGE---------------------------------------------------------------------------------
        DEBT TO EQUITY  mrq  {trj(le['debt to equity']['mrq'])} |{trj(le['debt to equity'][fy[0]])} |{trj(le['debt to equity'][fy[1]])} |{trj(le['debt to equity'][fy[2]])} |{trj(le['debt to equity'][fy[3]])} |
        DEBT TO ASSETS  mrq  {trj(le['debt to assets']['mrq'])} |{trj(le['debt to assets'][fy[0]])} |{trj(le['debt to assets'][fy[1]])} |{trj(le['debt to assets'][fy[2]])} |{trj(le['debt to assets'][fy[3]])} |
INTERST COVERAGE RATIO  mrq  {trj(le['interest coverage ratio']['mrq'])} |{trj(le['interest coverage ratio'][fy[0]])} |{trj(le['interest coverage ratio'][fy[1]])} |{trj(le['interest coverage ratio'][fy[2]])} |{trj(le['interest coverage ratio'][fy[3]])} |

EFFICIENCY-------------------------------------------------------------------------------
    INVENTORY TURNOVER  ttm  {trj(e['inventory turnover']['ttm'])} |{trj(e['inventory turnover'][fy[0]])} |{trj(e['inventory turnover'][fy[1]])} |{trj(e['inventory turnover'][fy[2]])} |{'-'.rjust(10)} |
  RECEIVABLES TURNOVER  ttm  {trj(e['receivables turnover']['ttm'])} |{trj(e['receivables turnover'][fy[0]])} |{trj(e['receivables turnover'][fy[1]])} |{trj(e['receivables turnover'][fy[2]])} |{'-'.rjust(10)} |
     PAYABLES TURNOVER  ttm  {trj(e['payables turnover']['ttm'])} |{trj(e['payables turnover'][fy[0]])} |{trj(e['payables turnover'][fy[1]])} |{trj(e['payables turnover'][fy[2]])} |{'-'.rjust(10)} |
                   DIO  ttm  {trj(e['dio']['ttm'])} |{trj(e['dio'][fy[0]])} |{trj(e['dio'][fy[1]])} |{trj(e['dio'][fy[2]])} |{'-'.rjust(10)} |
                   DSO  ttm  {trj(e['dso']['ttm'])} |{trj(e['dso'][fy[0]])} |{trj(e['dso'][fy[1]])} |{trj(e['dso'][fy[2]])} |{'-'.rjust(10)} |
                   DPO  ttm  {trj(e['dpo']['ttm'])} |{trj(e['dpo'][fy[0]])} |{trj(e['dpo'][fy[1]])} |{trj(e['dpo'][fy[2]])} |{'-'.rjust(10)} |
 CASH CONVERSION CYCLE  ttm  {trj(e['cash conversion cycle']['ttm'])} |{trj(e['cash conversion cycle'][fy[0]])} |{trj(e['cash conversion cycle'][fy[1]])} |{trj(e['cash conversion cycle'][fy[2]])} |{'-'.rjust(10)} |

CASH FLOW--------------------------------------------------------------------------------
            FCFF.DA.WC  ttm  {icrj(cf['fcff_DA.WC']['ttm'])} |{icrj(cf['fcff_DA.WC'][fy[0]])} |{icrj(cf['fcff_DA.WC'][fy[1]])} |{icrj(cf['fcff_DA.WC'][fy[2]])} |{icrj(cf['fcff_DA.WC'][fy[3]])} |
    FCFF.DA.WC.NonCash  ttm  {icrj(cf['fcff_DA.WC.otherNonCash']['ttm'])} |{icrj(cf['fcff_DA.WC.otherNonCash'][fy[0]])} |{icrj(cf['fcff_DA.WC.otherNonCash'][fy[1]])} |{icrj(cf['fcff_DA.WC.otherNonCash'][fy[2]])} |{icrj(cf['fcff_DA.WC.otherNonCash'][fy[3]])} |
            FCFE.DA.WC  ttm  {icrj(cf['fcfe_DA.WC']['ttm'])} |{icrj(cf['fcfe_DA.WC'][fy[0]])} |{icrj(cf['fcfe_DA.WC'][fy[1]])} |{icrj(cf['fcfe_DA.WC'][fy[2]])} |{icrj(cf['fcfe_DA.WC'][fy[3]])} |
    FCFE.DA.WC.NonCash  ttm  {icrj(cf['fcfe_DA.WC.otherNonCash']['ttm'])} |{icrj(cf['fcfe_DA.WC.otherNonCash'][fy[0]])} |{icrj(cf['fcfe_DA.WC.otherNonCash'][fy[1]])} |{icrj(cf['fcfe_DA.WC.otherNonCash'][fy[2]])} |{icrj(cf['fcfe_DA.WC.otherNonCash'][fy[3]])} |
''')

    def topgl(self, display: str = 'json'): # IN PROGRESS
        valid_params = {'valid_display': ['json', 'pretty'],}
        
        params = {'display': display}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
print(equity('JNJ').timeseries())