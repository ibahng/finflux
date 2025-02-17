from datafetch.base_var import Config

import yfinance as yf # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore
from datetime import timedelta, datetime

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
class bond:
#------------------------------------------------------------------------------------------
    def nonUS_10Y(self, country: str = 'KR', period: str = '5y'):
        valid_params = {'valid_country': ['KR', 'AT', 'CL', 'CZ', 'GR', 'FI', 'ZA', 'NL', 'SK', 'NZ', 'LU', 'PL', 'SI', 'CH', 'DE', 'CA', 'JP', 'DK', 'BE', 'FR', 'NO', 'PT', 'IT', 'GB', 'ES', 'IE', 'AU', 'SE', 'MX', 'HU', 'IS', 'RU'],
                        'valid_period': ['1y', '2y', '5y', '10y', 'max']}
        
        params = {'country': country,
                  'period': period}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        ISO_3166 = {
            'KR': 'South Korea',
            'AT': 'Austria',
            'US': 'United States',
            'CL': 'Chile',
            'CZ': 'Czech Republic',
            'GR': 'Greece',
            'FI': 'Finland',
            'ZA': 'South Africa',
            'NL': 'Netherlands',
            'SK': 'Slovak Republic',
            'NZ': 'New Zealand',
            'LU': 'Luxembourg',
            'PL': 'Poland',
            'SI': 'Slovenia',
            'CH': 'Switzerland',
            'DE': 'Germany',
            'CA': 'Canada',
            'JP': 'Japan',
            'DK': 'Denmark',
            'BE': 'Belgium',
            'FR': 'France',
            'NO': 'Norway',
            'PT': 'Portugal',
            'IT': 'Italy',
            'GB': 'United Kingdom',
            'ES': 'Spain',
            'IE': 'Ireland',
            'AU': 'Australia',
            'SE': 'Sweden',
            'MX': 'Mexico',
            'HU': 'Hungary',
            'IS': 'Iceland',
            'RU': 'Russia'
        }

        FRED_IDs = {}
        for ISO in ISO_3166.keys():
            FRED_IDs[ISO] = f'IRLTLT01{ISO}M156N'

        period_points = {
            '1y': -12,
            '2y': -24,
            '5y': -60,
            '10y': -120,
        }

        if Config.fred_apikey is None:
            raise MissingConfigObject('Missing fred_apikey. Please set your FRED api key using the set_config() function.')
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        id = FRED_IDs[country]

        FRED_url = f'https://api.stlouisfed.org/fred/series/observations?series_id={id}&api_key={Config.fred_apikey}&file_type=json'
        FRED_bond = requests.get(FRED_url).json()
        #----------------------------------------------------------------------------------

        def is_numeric(str):
            try:
                float(str)
                return True
            except ValueError:
                return False
        
        #PARAMETER - PERIOD ================================================================
        data = {}
        if period == 'max':
            for data_point in FRED_bond['observations']:
                data[data_point['date']] = (float(data_point['value']) if is_numeric(data_point['value']) else np.nan)
        else:
            for data_point in FRED_bond['observations'][period_points[period]:]:
                data[data_point['date']] = (float(data_point['value']) if is_numeric(data_point['value']) else np.nan)

        output = pd.DataFrame.from_dict(data, orient='index', columns=[f'{ISO_3166[country]} 10Y'])
        output.index = pd.to_datetime(output.index)

        return output
#------------------------------------------------------------------------------------------
    def US(self, display: str = 'json', maturity: str = '10y', period: str = '5y'):
        valid_params = {'valid_display': ['json', 'pretty'],
                        'valid_maturity': ['1mo', '3mo', '6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y'],
                        'valid_period' : ['1mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']}
        
        params = {'display': display,
                  'maturity': maturity,
                  'valid_period': period}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        FRED_IDs = {
            '1mo': 'DGS1MO',
            '3mo': 'DGS3MO',
            '6mo': 'DGS6MO',
            '1y': 'DGS1',
            '2y': 'DGS2',
            '3y': 'DGS3',
            '5y': 'DGS5',
            '7y': 'DGS7',
            '10y': 'DGS10',
            '20y': 'DGS20',
            '30y': 'DGS30'
        }    

        period_points = {
            '1mo': -21,
            '6mo': -126,
            '1y': -252,
            '2y': -504,
            '5y': -1260,
            '10y': -2520,
        }

        if Config.fred_apikey is None:
            raise MissingConfigObject('Missing fred_apikey. Please set your FRED api key using the set_config() function.')
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        id = FRED_IDs[maturity]

        FRED_url = f'https://api.stlouisfed.org/fred/series/observations?series_id={id}&api_key={Config.fred_apikey}&file_type=json'
        FRED_yield = requests.get(FRED_url).json()

        current_year = pd.Timestamp.now().year
        #----------------------------------------------------------------------------------

        def is_numeric(str):
            try:
                float(str)
                return True
            except ValueError:
                return False
        
        #PARAMETER - PERIOD ================================================================  
        data = {}
        if period == 'max':
            for data_point in FRED_yield['observations']:
                data[data_point['date']] = (float(data_point['value']) if is_numeric(data_point['value']) else np.nan)

        elif period == 'ytd':
            for data_point in FRED_yield['observations'][-260:]:
                if data_point['date'][0:4] == str(current_year):
                    data[data_point['date']] = (float(data_point['value']) if is_numeric(data_point['value']) else np.nan)

        else:
            for data_point in FRED_yield['observations'][period_points[period]:]:
                data[data_point['date']] = (float(data_point['value']) if is_numeric(data_point['value']) else np.nan)

        output = pd.DataFrame.from_dict(data, orient='index', columns=[f'US {maturity.upper()}'])
        output.index = pd.to_datetime(output.index)

        return output
#------------------------------------------------------------------------------------------
    def US_eod(self, display: str = 'json', maturity: str = '10y'):
        valid_params = {'valid_display': ['json', 'pretty'],
                        'valid_maturity': ['1mo', '3mo', '6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y']}
        
        params = {'display': display,
                  'maturity': maturity,}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
            
        FRED_IDs = {
            '1mo': 'DGS1MO',
            '3mo': 'DGS3MO',
            '6mo': 'DGS6MO',
            '1y': 'DGS1',
            '2y': 'DGS2',
            '3y': 'DGS3',
            '5y': 'DGS5',
            '7y': 'DGS7',
            '10y': 'DGS10',
            '20y': 'DGS20',
            '30y': 'DGS30'
        }
        
        if Config.fred_apikey is None:
            raise MissingConfigObject('Missing fred_apikey. Please set your FRED api key using the set_config() function.')
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        id = FRED_IDs[maturity]

        FRED_url = f'https://api.stlouisfed.org/fred/series/observations?series_id={id}&api_key={Config.fred_apikey}&file_type=json'
        FRED_yield = requests.get(FRED_url).json()
        #----------------------------------------------------------------------------------

        def is_numeric(str):
            try:
                float(str)
                return True
            except ValueError:
                return False

        #JSON FORMAT DATA
        eod_data = {
            'country': 'United States',
            'maturity': maturity.upper(),
            'date': FRED_yield['observations'][-1]['date'],
            'yield': (float(FRED_yield['observations'][-1]['value']) if is_numeric(FRED_yield['observations'][-1]['value']) else np.nan)
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = eod_data
            return output
        if display == 'pretty':
            output = f''' COUNTRY - United States
MATURITY - {eod_data['maturity']}
    DATE - {eod_data['date']}
   YIELD - {eod_data['yield']}'''
            print(output)
#------------------------------------------------------------------------------------------
    def US_quote(self, display: str = 'json', maturity: str = '10y'):
        valid_params = {'valid_display': ['json', 'pretty'],
                        'valid_maturity': ['1mo', '3mo', '6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y']}
        
        params = {'display': display,
                  'maturity': maturity,}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        if Config.fred_apikey is None:
            raise MissingConfigObject('Missing fred_apikey. Please set your FRED api key using the set_config() function.')
        
        #RAW DATA/OBSERVATIONS--------------------------------------------------------------
        US_timeseries = bond().US(display='pretty', maturity=maturity, period='10y')
        
        US_eod = bond().US_eod(display='json', maturity=maturity)['yield']
        
        current_year = pd.Timestamp.now().year
        #-----------------------------------------------------------------------------------
        
        #JSON FORMAT DATA
        quote_data = {
            'identifier': f'US {maturity.upper()} Treasury Bond Yield',
            'ttm': {
                'high': round(float((US_timeseries.iloc[-252:].max()).iloc[0]),2),
                'low': round(float((US_timeseries.iloc[-252:].min()).iloc[0]),2)
            },
            'percent change': {
                '5y': float(((US_eod/US_timeseries.iloc[-1260]) - 1).iloc[0] if pd.notna(US_timeseries.iloc[-1260].iloc[0]) else ((US_eod/US_timeseries.iloc[-1260]) - 1).iloc[1]),
                '1y': float(((US_eod/US_timeseries.iloc[-252]) - 1).iloc[0] if pd.notna(US_timeseries.iloc[-252].iloc[0]) else ((US_eod/US_timeseries.iloc[-252]) - 1).iloc[1]),
                'ytd': float(((US_eod/US_timeseries[US_timeseries.index.year == current_year].iloc[0]) - 1).iloc[0] if pd.notna(US_timeseries[US_timeseries.index.year == current_year].iloc[0].iloc[0]) else ((US_eod/US_timeseries[US_timeseries.index.year == current_year].iloc[1]) - 1).iloc[0]),
                '6m': float(((US_eod/US_timeseries.iloc[-126]) - 1).iloc[0] if pd.notna(US_timeseries.iloc[-126].iloc[0]) else ((US_eod/US_timeseries.iloc[-126]) - 1).iloc[1]),
                '1m': float(((US_eod/US_timeseries.iloc[-21]) - 1).iloc[0] if pd.notna(US_timeseries.iloc[-21].iloc[0]) else ((US_eod/US_timeseries.iloc[-21]) - 1).iloc[1]),
                '5d': float(((US_eod/US_timeseries.iloc[-5]) - 1).iloc[0] if pd.notna(US_timeseries.iloc[-5].iloc[0]) else ((US_eod/US_timeseries.iloc[-5]) - 1).iloc[1])
            },
            '50d average price': float((US_timeseries.iloc[-50:].mean()).iloc[0]),
            '200d average price': float((US_timeseries.iloc[-200:].mean()).iloc[0])
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = quote_data
            return output
        elif display == 'pretty':
            output = f'''
{quote_data['identifier']} Quote

TTM HIGH/LOW----------------------------
         HIGH --  {round(quote_data['ttm']['high'],2):,}
          LOW --  {round(quote_data['ttm']['low'],2):,}
PERCENT CHANGE--------------------------
       5 YEAR -- {' ' if pd.isna(quote_data['percent change']['5y']) or quote_data['percent change']['5y']>0 else ''}{round(quote_data['percent change']['5y'] * 100,2)}%
       1 YEAR -- {' ' if pd.isna(quote_data['percent change']['1y']) or quote_data['percent change']['1y']>0 else ''}{round(quote_data['percent change']['1y'] * 100,2)}%
          YTD -- {' ' if pd.isna(quote_data['percent change']['ytd']) or quote_data['percent change']['ytd']>0 else ''}{round(quote_data['percent change']['ytd'] * 100,2)}%
      6 MONTH -- {' ' if pd.isna(quote_data['percent change']['6m']) or quote_data['percent change']['6m']>0 else ''}{round(quote_data['percent change']['6m'] * 100,2)}%
      1 MONTH -- {' ' if pd.isna(quote_data['percent change']['1m']) or quote_data['percent change']['1m']>0 else ''}{round(quote_data['percent change']['1m'] * 100,2)}%
        5 DAY -- {' ' if pd.isna(quote_data['percent change']['5d']) or quote_data['percent change']['5d']>0 else ''}{round(quote_data['percent change']['5d'] * 100,2)}%
MOVING AVERAGES-------------------------
 50 DAY YIELD --  {round(quote_data['50d average price'],2)}
200 DAY YIELD --  {round(quote_data['200d average price'],2)}
'''
            print(output)
#------------------------------------------------------------------------------------------
    def filler():
        pass