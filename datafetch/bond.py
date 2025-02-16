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
    def nonUS_10Y(self, display: str = 'json', country: str = 'US', period: str = '5y'):
        valid_params = {'valid_display': ['json', 'pretty'],
                        'valid_country': ['KR', 'AT', 'US', 'CL', 'CZ', 'GR', 'FI', 'ZA', 'NL', 'SK', 'NZ', 'LU', 'PL', 'SI', 'CH', 'DE', 'CA', 'JP', 'DK', 'BE', 'FR', 'NO', 'PT', 'IT', 'GB', 'ES', 'IE', 'AU', 'SE', 'MX', 'HU', 'IS', 'RU'],
                        'valid_period': ['1y', '2y', '5y', '10y', 'max']}
        
        params = {'display': display,
                  'country': country,
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

        #JSON FORMAT DATA
        nonUS_10Y_data = {
            'country': ISO_3166[country],
            'start date': FRED_bond['observations'][0]['date'],
            'end date': FRED_bond['observations'][-1]['date'],
            'data count': len(data),
            'data': data
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = nonUS_10Y_data
        if display == 'pretty':
            output = pd.DataFrame.from_dict(data, orient='index', columns=[f'{ISO_3166[country]} 10Y'])

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

            start_date = FRED_yield['observations'][0]['date']
            end_date = FRED_yield['observations'][-1]['date']

        elif period == 'ytd':
            for data_point in FRED_yield['observations'][-260:]:
                if data_point['date'][0:4] == str(current_year):
                    data[data_point['date']] = (float(data_point['value']) if is_numeric(data_point['value']) else np.nan)

            start_date = min(data.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
            end_date = max(data.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))

        else:
            for data_point in FRED_yield['observations'][period_points[period]:]:
                data[data_point['date']] = (float(data_point['value']) if is_numeric(data_point['value']) else np.nan)

            start_date = FRED_yield['observations'][period_points[period]:][0]['date']
            end_date = FRED_yield['observations'][period_points[period]:][-1]['date']

        #JSON FORMAT DATA
        US_yield_data = {
            'country': 'United States',
            'maturity': maturity.upper(),
            'start date': start_date,
            'end date': end_date,
            'data count': len(data),
            'data': data
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = US_yield_data
        if display == 'pretty':
            output = pd.DataFrame.from_dict(data, orient='index', columns=[f'US {maturity.upper()}'])

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
    def filler():
        pass