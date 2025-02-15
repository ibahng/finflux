from datafetch.base_var import Config

import yfinance as yf # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore
from datetime import timedelta

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
    def nonUS_10Y(self, display: str = 'json', country: str = 'US'):
        valid_params = {'display': ['json', 'pretty'],
                        'country': ['KR', 'AT', 'US', 'CL', 'CZ', 'GR', 'FI', 'ZA', 'NL', 'SK', 'NZ', 'LU', 'PL', 'SI', 'CH', 'DE', 'CA', 'JP', 'DK', 'BE', 'FR', 'NO', 'PT', 'IT', 'GB', 'ES', 'IE', 'AU', 'SE', 'MX', 'HU', 'IS', 'RU']}
        
        params = {'display': display,
                  'country': country}

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

        if Config.fred_apikey is None:
            raise MissingConfigObject('Missing fred_apikey. Please set your FRED api key using the set_config() function.')
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        id = FRED_IDs[country]

        FRED_url = f'https://api.stlouisfed.org/fred/series/observations?series_id={id}&api_key={Config.fred_apikey}&file_type=json'
        FRED_bond = requests.get(FRED_url).json()
        #----------------------------------------------------------------------------------

        data = {}
        for data_point in FRED_bond['observations']:
            data[data_point['date']] = float(data_point['value'])

        #JSON FORMAT DATA
        nonUS_10Y_data = {
            'country': ISO_3166[country],
            'start date': FRED_bond['observations'][0]['date'],
            'end date': FRED_bond['observations'][-1]['date'],
            'data count': FRED_bond['count'],
            'data': data
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = nonUS_10Y_data
        if display == 'pretty':
            output = pd.DataFrame.from_dict(data, orient='index', columns=[f'{ISO_3166[country]} Monthly 10Y Bond Yield'])

        return output
#------------------------------------------------------------------------------------------
    def US(display: str = 'json'):
        pass