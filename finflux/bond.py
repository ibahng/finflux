from finflux.base_var import Config

import yfinance as yf # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import BDay
import investpy as ip # type: ignore

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

class InvalidCountryMaturity(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class ChartReadabilityError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

#------------------------------------------------------------------------------------------
class bond:
#------------------------------------------------------------------------------------------
    def sovereign_timeseries(self, display: str = 'table', period: str = '5y', start: str = None, end: str = None, interval: str = '1d', data: str = 'all', maturity: str = '10y', country: str = 'US', show: str = True, save: str = False): 
        valid_params = {'valid_display': ['table', 'json', 'line'],
                        'valid_period': ['6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        'valid_interval': ['1d', '1wk', '1mo'],
                        'valid_data' : ['open', 'high', 'low', 'close', 'all'],
                        'valid_maturity': ['6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y'],
                        'valid_country' : ['AU', 'AT', 'BH', 'BD', 'BE', 'BR', 'BG', 'CA', 'CL', 'CN', 'CO', 'CI', 'HR', 'CY', 'CZ', 'DK', 'EG', 'FI', 'FR', 'DE', 'GR', 'HK', 'HU', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JP', 'KZ', 'KE', 'LV', 'LT', 'MY', 'MT', 'MU', 'MX', 'MA', 'NA', 'NL', 'NZ', 'NG', 'NO', 'PK', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU', 'RS', 'SG', 'SK', 'SI', 'ZA', 'KR', 'ES', 'LK', 'SE', 'CH', 'TW', 'TH', 'TR', 'UG', 'UA', 'GB', 'US', 'VN', 'ZM'],
                        'valid_show' : [True, False],
                        'valid_save' : [True, False]}
        
        params = {'display': display,
                  'period': period,
                  'interval': interval,
                  'data': data,
                  'maturity': maturity,
                  'country': country,
                  'show': show,
                  'save': save}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        iso_country_dict = {
            'AU': ['Australia', 'Australia'],
            'AT': ['Austria', 'Austria'],
            'BH': ['Bahrain', 'Bahrain'],
            'BD': ['Bangladesh', 'Bangladesh'],
            'BE': ['Belgium', 'Belgium'],
            'BR': ['Brazil', 'Brazil'],
            'BG': ['Bulgaria', 'Bulgaria'],
            'CA': ['Canada', 'Canada'],
            'CL': ['Chile', 'Chile'],
            'CN': ['China', 'China'],
            'CO': ['Colombia', 'Colombia'],
            'CI': ["Cote D'Ivoire", "Cote d'Ivoire"],
            'HR': ['Croatia', 'Croatia'],
            'CY': ['Cyprus', 'Cyprus'],
            'CZ': ['Czech Republic', 'Czech Republic'],
            'DK': ['Denmark', 'Denmark'],
            'EG': ['Egypt', 'Egypt'],
            'FI': ['Finland', 'Finland'],
            'FR': ['France', 'France'],
            'DE': ['Germany', 'Germany'],
            'GR': ['Greece', 'Greece'],
            'HK': ['Hong Kong', 'Hong Kong'],
            'HU': ['Hungary', 'Hungary'],
            'IS': ['Iceland', 'Iceland'],
            'IN': ['India', 'India'],
            'ID': ['Indonesia', 'Indonesia'],
            'IE': ['Ireland', 'Ireland'],
            'IL': ['Israel', 'Israel'],
            'IT': ['Italy', 'Italy'],
            'JP': ['Japan', 'Japan'],
            'KZ': ['Kazakhstan', 'Kazakhstan'],
            'KE': ['Kenya', 'Kenya'],
            'LV': ['Latvia', 'Latvia'],
            'LT': ['Lithuania', 'Lithuania'],
            'MY': ['Malaysia', 'Malaysia'],
            'MT': ['Malta', 'Malta'],
            'MU': ['Mauritius', 'Mauritius'],
            'MX': ['Mexico', 'Mexico'],
            'MA': ['Morocco', 'Morocco'],
            'NA': ['Namibia', 'Namibia'],
            'NL': ['Netherlands', 'Netherlands'],
            'NZ': ['New Zealand', 'New Zealand'],
            'NG': ['Nigeria', 'Nigeria'],
            'NO': ['Norway', 'Norway'],
            'PK': ['Pakistan', 'Pakistan'],
            'PE': ['Peru', 'Peru'],
            'PH': ['Philippines', 'Philippines'],
            'PL': ['Poland', 'Poland'],
            'PT': ['Portugal', 'Portugal'],
            'QA': ['Qatar', 'Qatar'],
            'RO': ['Romania', 'Romania'],
            'RU': ['Russia', 'Russia'],
            'RS': ['Serbia', 'Serbia'],
            'SG': ['Singapore', 'Singapore'],
            'SK': ['Slovakia', 'Slovakia'],
            'SI': ['Slovenia', 'Slovenia'],
            'ZA': ['South Africa', 'South Africa'],
            'KR': ['South Korea', 'South Korea'],
            'ES': ['Spain', 'Spain'],
            'LK': ['Sri Lanka', 'Sri Lanka'],
            'SE': ['Sweden', 'Sweden'],
            'CH': ['Switzerland', 'Switzerland'],
            'TW': ['Taiwan', 'Taiwan'],
            'TH': ['Thailand', 'Thailand'],
            'TR': ['Turkey', 'Turkey'],
            'UG': ['Uganda', 'Uganda'],
            'UA': ['Ukraine', 'Ukraine'],
            'GB': ['United Kingdom', 'U.K.'],
            'US': ['United States', 'U.S.'],
            'VN': ['Vietnam', 'Vietnam'],
            'ZM': ['Zambia', 'Zambia']
        }

        interval_dict = {
            '1d': 'Daily',
            '1wk': 'Weekly',
            '1mo': 'Monthly',
        }

        #if both start and end parameters are filled, then it will override the period parameter
        if start == None or end == None:
            today = date.today().strftime('%d/%m/%Y')

            if period not in ('ytd', 'max'):
                from_date_dict = {
                    '6mo': (date.today() - relativedelta(months=6)).strftime('%d/%m/%Y'),
                    '1y': (date.today() - relativedelta(years=1)).strftime('%d/%m/%Y'),
                    '2y': (date.today() - relativedelta(years=2)).strftime('%d/%m/%Y'),
                    '5y': (date.today() - relativedelta(years=5)).strftime('%d/%m/%Y'),
                    '10y': (date.today() - relativedelta(years=10)).strftime('%d/%m/%Y'),
                }
                try:
                    yield_df = ip.bonds.get_bond_historical_data(bond = f'{iso_country_dict[country][1]} {maturity.upper()}',
                                                                from_date = from_date_dict[period],
                                                                to_date = today,
                                                                interval = interval_dict[interval])
                except RuntimeError:
                    raise InvalidCountryMaturity(f'Inputted maturity {maturity.upper()} does not exist for {iso_country_dict[country][0]}. Please try a different country maturity pair.')

            elif period == 'ytd':
                try:
                    yield_df = ip.bonds.get_bond_historical_data(bond = f'{iso_country_dict[country][1]} {maturity.upper()}',
                                                                from_date = (date.today() - relativedelta(years=1)).strftime('%d/%m/%Y'),
                                                                to_date = today,
                                                                interval = interval_dict[interval])
                    
                    current_year = datetime.now().year
                    yield_df = yield_df[yield_df.index.year == current_year]
                except RuntimeError:
                    raise InvalidCountryMaturity(f'Inputted maturity {maturity.upper()} does not exist for {iso_country_dict[country][0]}. Please try a different country maturity pair.')
            elif period == 'max':
                try:
                    yield_df = ip.bonds.get_bond_historical_data(bond = f'{iso_country_dict[country][1]} {maturity.upper()}',
                                                                from_date = '01/01/1980',
                                                                to_date = today,
                                                                interval = interval_dict[interval])
                except RuntimeError:
                    raise InvalidCountryMaturity(f'Inputted maturity {maturity.upper()} does not exist for {iso_country_dict[country][0]}. Please try a different country maturity pair.')

        elif isinstance(start, str) and isinstance(end, str):
            try:
                yield_df = ip.bonds.get_bond_historical_data(bond = f'{iso_country_dict[country][1]} {maturity.upper()}',
                                                            from_date = f'{start[8:]}/{start[5:7]}/{start[0:4]}',
                                                            to_date = f'{end[8:]}/{end[5:7]}/{end[0:4]}',
                                                            interval = interval_dict[interval])
            except RuntimeError:
                raise InvalidCountryMaturity(f'Inputted maturity {maturity.upper()} does not exist for {iso_country_dict[country][0]}. Please try a different country maturity pair.')
        #----------------------------------------------------------------------------------
        
        #STANDARDIZING THE COLUMN NAMES
        yield_df.columns = [
            f'{country} {maturity.upper()} Open',
            f'{country} {maturity.upper()} High',
            f'{country} {maturity.upper()} Low',
            f'{country} {maturity.upper()} Close'
        ]

        #PARAMETER - DATA =================================================================
        if data in ('open', 'high', 'low', 'close'):
            yield_df = yield_df[f'{country} {maturity.upper()} {data.capitalize()}']

        #PARAMETER - DISPLAY ==============================================================
        if display == 'table':
            output = yield_df
            return output
        elif display == 'json':
            yield_df.index = yield_df.index.strftime('%Y-%m-%d')
            
            yield_json_list = []
            if data == 'all':
                for index, row in yield_df.iterrows():
                    a = {
                        'Date': index,
                        f'{country} {maturity.upper()} Open': float(row[f'{country} {maturity.upper()} Open']),
                        f'{country} {maturity.upper()} High': float(row[f'{country} {maturity.upper()} High']),
                        f'{country} {maturity.upper()} Low': float(row[f'{country} {maturity.upper()} Low']),
                        f'{country} {maturity.upper()} Close': float(row[f'{country} {maturity.upper()} Close']),
                    }
                    yield_json_list.append(a)
            elif data != 'all':
                for index, row in yield_df.iterrows():
                    a = {
                        'Date': index,
                        f'{country} {maturity.upper()} {data.title()}': row[f'{country} {maturity.upper()} {data.title()}']
                    }
                    yield_json_list.append(a)
            
            output = yield_json_list
            return output
        elif display == 'line':
            if data == 'all':
                raise ChartReadabilityError('For optimal plot readability, only one type of OHLC yield data can be selected at a time. Currently, multiple options are selected. Please choose a single data parameter.')
            
            elif data != 'all':
                fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)

                ax.plot(yield_df.index, yield_df)
                
                first_date = yield_df.index[0].strftime('%b %Y')
                last_date = yield_df.index[-1].strftime('%b %Y')

                ax.set_title(f'{iso_country_dict[country][0]} {maturity.upper()} Bond Yield {interval_dict[interval]} {data.capitalize()} — ({first_date} - {last_date})', fontsize=6.5, loc='left', pad=4, fontname='Arial', weight='bold')

                #PLOT AESTHETICS---------------------------------------------------------------
                ax.set_facecolor('#E6F2FA') #BACKGROUND COLOR

                for spine in ax.spines.values(): # SPINES AKA EDGES
                    spine.set_visible(True)            # ensure visibility
                    spine.set_edgecolor('#7A7A7A')    # gray color
                    spine.set_linewidth(0.15)          # adjust thickness

                ax.minorticks_on() #need to turn on minor ticks to plot minor grid lines
                ax.tick_params(which="minor", axis='both', direction='out', color='white', width=0) #minor ticks invisible
                ax.tick_params(which="major", axis='both', direction='out', width=1, zorder=3) #major ticks

                ax.grid(which='major', color='#FFFFFF', linestyle='-', linewidth=0.8, zorder=0) #major grid lines
                ax.grid(which='minor', color='#FFFFFF', linestyle='--', linewidth=0.4, zorder=0) #minor grid lines

                ax.yaxis.tick_right()            # ticks appear on the right
                ax.yaxis.set_label_position("right")  # y-axis label moves to the right

                for label in ax.get_xticklabels() + ax.get_yticklabels(): #sets all label fonts to 7 and Arial
                    label.set_fontsize(7)
                    label.set_fontname('Arial')

                ax.set_axisbelow(True) #making the grid and everything below the actual data line
                #SAVE--------------------------------------------------------------------------
                if save:
                    plt.savefig(f'{country}{maturity.upper()}_Simple{interval_dict[interval]}{data.capitalize()}_{yield_df.index[0].strftime('%b%Y')}_{yield_df.index[-1].strftime('%b%Y')}.png', dpi=300, bbox_inches='tight')

                #SHOW--------------------------------------------------------------------------
                if show:
                    plt.show()
                elif show == False:
                    plt.close(fig)
#------------------------------------------------------------------------------------------
    def bond_candle(self, period: str = '6mo', start: str = None, end: str = None, interval: str = '1d', sma: list = None, bollinger: list = None, o_label: bool = True, h_label: bool = True, l_label: bool = True, c_label: bool = True, legend: bool = False, title: bool = True, maturity: str = '10y', country: str = 'US', show: str = True, save: str = False):
        valid_params = {'valid_period' : ['6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        'valid_interval' : ['1d', '1wk', '1mo'],
                        'valid_o_label' : [True, False],
                        'valid_h_label' : [True, False],
                        'valid_l_label' : [True, False],
                        'valid_c_label' : [True, False],
                        'valid_legend': [True, False],
                        'valid_title': [True, False],
                        'valid_show' : [True, False],
                        'valid_save' : [True, False],
                        'valid_maturity': ['6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y'],
                        'valid_country' : ['AU', 'AT', 'BH', 'BD', 'BE', 'BR', 'BG', 'CA', 'CL', 'CN', 'CO', 'CI', 'HR', 'CY', 'CZ', 'DK', 'EG', 'FI', 'FR', 'DE', 'GR', 'HK', 'HU', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JP', 'KZ', 'KE', 'LV', 'LT', 'MY', 'MT', 'MU', 'MX', 'MA', 'NA', 'NL', 'NZ', 'NG', 'NO', 'PK', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU', 'RS', 'SG', 'SK', 'SI', 'ZA', 'KR', 'ES', 'LK', 'SE', 'CH', 'TW', 'TH', 'TR', 'UG', 'UA', 'GB', 'US', 'VN', 'ZM']}
        
        params = {'period': period,
                  'interval': interval,
                  'o_label': o_label,
                  'h_label': h_label,
                  'l_label': l_label,
                  'c_label': c_label,
                  'legend': legend,
                  'title': title,
                  'show': show,
                  'save': save,
                  'maturity': maturity,
                  'country': country}
        
        #SMA will be int or list from 10-300 inclusive
        #bollinger will be 0.1-3.0 SDs floats inclusive with 0.05 increments; only works when sma is an int
        
        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        #RAW DATA/OBSERVATIONS-------------------------------------------------------------
        data = self.sovereign_timeseries(display = 'table',
                                         period=period,
                                         start=start,
                                         end=end,
                                         interval=interval,
                                         data='all',
                                         maturity=maturity,
                                         country=country)
        data['DateNum'] = [x for x in range(0,len(data))]
        #----------------------------------------------------------------------------------

        #SETTING LIMITS ON NUMBER OF DATA DF ROWS POSSIBLE---------------------------------(this is to prevent overly cramped candlestick formatting)
        if len(data) > 265:
            raise ChartReadabilityError(f"Number of OHLC candles are capped at 265 to ensure plot readability. The current selection contains {len(data)} data points. Please reduce the time period or choose a larger interval.")
            #1d interval and 1y period is ~262 datapoints
            #1wk interval and 5y period is ~250 datapoints
            #1mo interval and 10y period is well below the cap

        #SETTING LIMITS ON SMA AND BOLLINGER BAND SD---------------------------------------
        #SMA 10-300 inclusive ints
        if isinstance(sma, list):
            if len(sma) > 5:
                raise ChartReadabilityError(f"Number of SMA lines are capped at 5 to ensure plot readability. The current selection contains {len(sma)} SMA lines. Please reduce the number of SMA lines.")
            for sma_i in sma:
                if sma_i > 300 or sma_i < 10:
                    raise InvalidParameterError(f"Invalid sma parameter '{sma_i}'. "
                                            f"Please choose an integer between 10 and 300 (inclusive)")

        #BB 0.1-3.0 inclusive floats
        if isinstance(bollinger, list):
            if len(sma) != len(bollinger):
                raise InvalidParameterError(f"Number of bollinger band standard deviation does not match the number of SMA lines. The current selection contains {len(sma)} SMA lines. Please match the number of bollinger band standard deviations to {len(sma)}.")
            for bollinger_i in bollinger:
                if bollinger_i != None:
                    if bollinger_i > 3 or bollinger_i < 0.1:
                        raise InvalidParameterError(f"Invalid bollinger parameter '{bollinger_i}'. "
                                                    f"Please choose an integer or float between 0.1 and 3 (inclusive)")

        #SETTING UP DATA DATAFRAME WITH OPTIONAL SMA AND BOLLINGER BAND COLUMN(S)----------
        if sma is not None:
            max_c_data = self.sovereign_timeseries(period='max', data='all', interval=interval, maturity=maturity, country=country)
            #creating sma columns in data dataframe based on bollinger condition
            if bollinger == None:
                for i in sma:
                    max_c_data[f'SMA {i}'] = max_c_data[f'{country} {maturity.upper()} Close'].rolling(window=i).mean()
                    data[f'SMA {i}'] = max_c_data[f'SMA {i}'].tail(len(data))
            elif isinstance(bollinger, list):
                for i, b in zip(sma, bollinger):
                    if b != None:
                        max_c_data[f'SMA {i}'] = max_c_data[f'{country} {maturity.upper()} Close'].rolling(window=i).mean()
                        data[f'SMA {i}'] = max_c_data[f'SMA {i}'].tail(len(data))
                        max_c_data[f'SD {i}'] = max_c_data[f'{country} {maturity.upper()} Close'].rolling(window=i).std()
                        data[f'bollinger_upper {i}'] = data[f'SMA {i}'] + (b * max_c_data[f'SD {i}'].tail(len(data)))
                        data[f'bollinger_lower {i}'] = data[f'SMA {i}'] - (b * max_c_data[f'SD {i}'].tail(len(data)))
                    elif b == None:
                        max_c_data[f'SMA {i}'] = max_c_data[f'{country} {maturity.upper()} Close'].rolling(window=i).mean()
                        data[f'SMA {i}'] = max_c_data[f'SMA {i}'].tail(len(data))

        #CREATING THE MAIN FIG AX PAIR ----------------------------------------------------
        fig, ax_p = plt.subplots(figsize=(10, 4.5), dpi=300)

        #PLOTTING THE MAIN OHLC CANDLESTICKS-----------------------------------------------
        if len(data) > 200:
            candle_width = 0.3
        elif len(data) > 150:
            candle_width = 0.4
        elif len(data) > 100:
            candle_width = 0.5
        elif len(data) > 50:
            candle_width = 0.6
        else:
            candle_width = 0.7
        
        for index, row in data.iterrows():
            color = 'green' if row[f'{country} {maturity.upper()} Close'] >= row[f'{country} {maturity.upper()} Open'] else 'red'
            #wick
            ax_p.vlines(row['DateNum'], row[f'{country} {maturity.upper()} Low'], row[f'{country} {maturity.upper()} High'], color=color, linewidth=0.25)
            #box
            ax_p.add_patch(plt.Rectangle(
                (row['DateNum'] - (candle_width/2), min(row[f'{country} {maturity.upper()} Open'], row[f'{country} {maturity.upper()} Close'])), # bottom left corner of the rectangle
                candle_width, # horizontal width of the rectangle
                abs(row[f'{country} {maturity.upper()} Close'] - row[f'{country} {maturity.upper()} Open']), #vertical height of the rectangle
                color=color #fill color of the rectangle
            ))

        #PLOTTING OPTIONAL SMA AND BOLLINGER BAND LINES------------------------------------
        if isinstance(sma, list):
            sma_colors = ["#1f77b4", "#ff7f0e", "#9467bd", "#8c564b", "#17becf"]
            if bollinger == None:
                for sma_number, sma_color in zip(sma, sma_colors):
                    ax_p.plot(data['DateNum'], data[f'SMA {sma_number}'], color = sma_color, linewidth = 0.6, label = f'SMA {sma_number}')
            elif isinstance(bollinger, list):
                for sma_number, sma_color, bollinger_number in zip(sma, sma_colors, bollinger):
                    if bollinger_number != None:
                        ax_p.plot(data['DateNum'], data[f'SMA {sma_number}'], color = sma_color, linewidth = 0.6, linestyle = '--', label = f'SMA {sma_number}')
                        ax_p.plot(data['DateNum'], data[f'bollinger_upper {sma_number}'], color = sma_color, linewidth = 0.4, linestyle = '-', label = f'BB ({sma_number}, {bollinger_number})')
                        ax_p.plot(data['DateNum'], data[f'bollinger_lower {sma_number}'], color = sma_color, linewidth = 0.4, linestyle = '-')
                        ax_p.fill_between(data['DateNum'], data[f'bollinger_lower {sma_number}'], data[f'bollinger_upper {sma_number}'], color = sma_color, alpha = 0.1)
                    elif bollinger_number == None:
                        ax_p.plot(data['DateNum'], data[f'SMA {sma_number}'], color = sma_color, linewidth = 0.6, label = f'SMA {sma_number}')

        #PLOTTING OPTIONAL OHLC LABELS-----------------------------------------------------
        label_bools = [o_label, h_label, l_label, c_label]

        ax_p_length = ax_p.get_xlim()[1] - ax_p.get_xlim()[0]

        label_vd_list = []

        if o_label:
            o_value, o_datenum = round(float(data[f'{country} {maturity.upper()} Open'].iloc[0]),2), (0-ax_p.get_xlim()[0])/ax_p_length
        else:
            o_value, o_datenum = None, None

        if h_label:
            h_value, h_datenum = round(data[f'{country} {maturity.upper()} High'].max(),2), (int(data.loc[data[f'{country} {maturity.upper()} High'].idxmax(), "DateNum"])-ax_p.get_xlim()[0])/ax_p_length
        else:
            h_value, h_datenum = None, None

        if l_label:
            l_value, l_datenum = round(data[f'{country} {maturity.upper()} Low'].min(),2), (int(data.loc[data[f'{country} {maturity.upper()} Low'].idxmin(), "DateNum"])-ax_p.get_xlim()[0])/ax_p_length
        else:
            l_value, l_datenum = None, None

        if c_label:
            c_value, c_datenum = round(float(data[f'{country} {maturity.upper()} Close'].iloc[-1]),2), (len(data)-1-ax_p.get_xlim()[0])/ax_p_length
        else:
            c_value, c_datenum = None, None

        label_vd_list.append([o_value, o_datenum, 'O'])
        label_vd_list.append([h_value, h_datenum, 'H'])
        label_vd_list.append([l_value, l_datenum, 'L'])
        label_vd_list.append([c_value, c_datenum, 'C'])

        for label_bool, label_vd in zip(label_bools, label_vd_list):
            if label_bool:
                ax_p.axhline(label_vd[0], xmin=label_vd[1], color="orange", ls="--", lw=0.6, alpha=0.6)  # guide line
                ax_p.text(
                    x=1, y=label_vd[0], 
                    s=f"{label_vd[2]}: {label_vd[0]}", 
                    va="center", ha="left",
                    backgroundcolor="white", 
                    bbox=dict(facecolor="lightblue", edgecolor="none", boxstyle="round,pad=0.2"),
                    fontsize=5.5,
                    transform=ax_p.get_yaxis_transform()  #this make the x parameter a value between 0 and 1, 0 meaning very left side of the plot and 1 being the right
                )

        #REPLACING XLABEL INTEGERS WITH DATESTRINGS----------------------------------------
        f_list = list(ax_p.get_xticks()[1:len(ax_p.get_xticks())-1])
        int_list = [int(x) for x in f_list]
        int_list

        date_label_list = []
        for i in int_list:
            diff = i - data['DateNum'].iloc[-1]

            interval_dict = { 
            '1d': BDay(diff),
            '1wk': pd.DateOffset(weeks=diff),
            '1mo': pd.DateOffset(months=diff)
        }
            if diff <= 0:
                date_label_list.append(data.index[i].strftime('%Y-%b-%d'))
            elif diff > 0:
                diff = i - data['DateNum'].iloc[-1]
                date = data.index[-1] + interval_dict[interval]
                
                date_label_list.append(date.strftime('%Y-%b-%d'))

        def date_tick_labels(ax):
            ax.set_xticks(int_list)
            ax.set_xticklabels(date_label_list)

        date_tick_labels(ax_p)

        #MAKING THE PLOT AESTHETIC---------------------------------------------------------
        def style_ax(ax):
            ax.set_facecolor('#fafafa') #BACKGROUND COLOR

            for spine in ax.spines.values(): # SPINES AKA EDGES
                spine.set_visible(True)            # ensure visibility
                spine.set_edgecolor('#7A7A7A')    # gray color
                spine.set_linewidth(0.5)          # adjust thickness

            ax.minorticks_on()
            ax.tick_params(which="minor", axis='both', direction='out', color='white') #minor ticks invisible

            ax.grid(which='major', color='#bfbfbf', linestyle='-', linewidth=0.35) #major grid lines
            ax.grid(which='minor', color='#bfbfbf', linestyle='--', linewidth=0.15) #minor grid lines

            ax.yaxis.tick_right()            # ticks appear on the right
            ax.yaxis.set_label_position("right")  # y-axis label moves to the right

            for label in ax.get_xticklabels() + ax.get_yticklabels(): #sets all label fonts to 7 and Arial
                label.set_fontsize(7)
                label.set_fontname('Arial')

            ax.set_axisbelow(True) #making the grid and everything below the actual data line

        style_ax(ax_p)
        ax_p.tick_params(which="major", axis='both', direction='in', width=0.7) #major ohlc chart ticks

        #OPTIONAL LEGEND-------------------------------------------------------------------
        if legend: ax_p.legend(fontsize=6, frameon=False, facecolor=None, borderaxespad=1.2)

        #OPTIONAL TITLE--------------------------------------------------------------------
        if title:
            iso_country_dict = {
                        'AU': 'Australia',
                        'AT': 'Austria',
                        'BH': 'Bahrain',
                        'BD': 'Bangladesh',
                        'BE': 'Belgium',
                        'BR': 'Brazil',
                        'BG': 'Bulgaria',
                        'CA': 'Canada',
                        'CL': 'Chile',
                        'CN': 'China',
                        'CO': 'Colombia',
                        'CI': "Cote D'Ivoire",
                        'HR': 'Croatia',
                        'CY': 'Cyprus',
                        'CZ': 'Czech Republic',
                        'DK': 'Denmark',
                        'EG': 'Egypt',
                        'FI': 'Finland',
                        'FR': 'France',
                        'DE': 'Germany',
                        'GR': 'Greece',
                        'HK': 'Hong Kong',
                        'HU': 'Hungary',
                        'IS': 'Iceland',
                        'IN': 'India',
                        'ID': 'Indonesia',
                        'IE': 'Ireland',
                        'IL': 'Israel',
                        'IT': 'Italy',
                        'JP': 'Japan',
                        'KZ': 'Kazakhstan',
                        'KE': 'Kenya',
                        'LV': 'Latvia',
                        'LT': 'Lithuania',
                        'MY': 'Malaysia',
                        'MT': 'Malta',
                        'MU': 'Mauritius',
                        'MX': 'Mexico',
                        'MA': 'Morocco',
                        'NA': 'Namibia',
                        'NL': 'Netherlands',
                        'NZ': 'New Zealand',
                        'NG': 'Nigeria',
                        'NO': 'Norway',
                        'PK': 'Pakistan',
                        'PE': 'Peru',
                        'PH': 'Philippines',
                        'PL': 'Poland',
                        'PT': 'Portugal',
                        'QA': 'Qatar',
                        'RO': 'Romania',
                        'RU': 'Russia',
                        'RS': 'Serbia',
                        'SG': 'Singapore',
                        'SK': 'Slovakia',
                        'SI': 'Slovenia',
                        'ZA': 'South Africa',
                        'KR': 'South Korea',
                        'ES': 'Spain',
                        'LK': 'Sri Lanka',
                        'SE': 'Sweden',
                        'CH': 'Switzerland',
                        'TW': 'Taiwan',
                        'TH': 'Thailand',
                        'TR': 'Turkey',
                        'UG': 'Uganda',
                        'UA': 'Ukraine',
                        'GB': 'United Kingdom',
                        'US': 'United States',
                        'VN': 'Vietnam',
                        'ZM': 'Zambia'
                    }
            
            interval_map = {
                '1d': 'Daily',
                '1wk': 'Weekly',
                '1mo': 'Monthly'
            }

            first_date = data.index[0].strftime('%b %Y')
            last_date = data.index[-1].strftime('%b %Y')
            ax_p.set_title(f'{iso_country_dict[country]} {maturity.upper()} Bond Yield — {interval_map[interval]} OHLC ({first_date} - {last_date})', fontsize=6.5, loc='left', pad=4, fontname='Arial', weight='bold')

        #SAVE------------------------------------------------------------------------------
        if save:
            plt.savefig(f'{country}{maturity.upper()}_{interval_map[interval]}CandleChart_{data.index[0].strftime('%b%Y')}_{data.index[-1].strftime('%b%Y')}.png', dpi=300, bbox_inches='tight')

        #SHOW------------------------------------------------------------------------------
        if show:
            plt.show()
        elif show == False:
            plt.close(fig)
#------------------------------------------------------------------------------------------
    def curve(self, display: str = 'line', country: str = 'US', eod_line: bool = True, three_month_line: bool = True, six_month_line: bool = True, show: str = True, save: str = False):
        valid_params = {'valid_display': ['json', 'table', 'line'],
                        'valid_country' : ['AU', 'AT', 'BH', 'BD', 'BE', 'BR', 'BG', 'CA', 'CL', 'CN', 'CO', 'CI', 'HR', 'CY', 'CZ', 'DK', 'EG', 'FI', 'FR', 'DE', 'GR', 'HK', 'HU', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JP', 'KZ', 'KE', 'LV', 'LT', 'MY', 'MT', 'MU', 'MX', 'MA', 'NA', 'NL', 'NZ', 'NG', 'NO', 'PK', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU', 'RS', 'SG', 'SK', 'SI', 'ZA', 'KR', 'ES', 'LK', 'SE', 'CH', 'TW', 'TH', 'TR', 'UG', 'UA', 'GB', 'US', 'VN', 'ZM'],
                        'valid_eod_line': [True, False],
                        'valid_three_month_line': [True, False],
                        'valid_six_month_line': [True, False],
                        'valid_show' : [True, False],
                        'valid_save' : [True, False]}
        
        params = {'display': display,
                  'country': country,
                  'eod_line': eod_line,
                  'three_month_line': three_month_line,
                  'six_month_line': six_month_line,
                  'show': show,
                  'save': save}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        maturity_list= ["6mo", "1y", "2y", "3y", "5y", "7y", "10y", "20y", "30y"]
        
        six_m_yields = []
        three_m_yields = []
        eod_yields = []

        for maturity in maturity_list:
            try:
                a = self.sovereign_timeseries(display='table', period='6mo', interval='1d', data='close', maturity=maturity, country=country)
                six_m_yields.append(float(a.iloc[0]))
                three_m_yields.append(float(a.iloc[int(len(a)/2)]))
                eod_yields.append(float(a.iloc[-1]))
            except InvalidCountryMaturity:
                a = np.nan
                six_m_yields.append(a)
                three_m_yields.append(a)
                eod_yields.append(a)
        #----------------------------------------------------------------------------------

        #JSON FORMAT DATA

        six_month_dict = {}
        three_month_dict = {}
        eod_dict = {}

        for maturity, six_m_yield in zip(maturity_list, six_m_yields):
            six_month_dict[maturity] = six_m_yield
        
        for maturity, three_m_yield in zip(maturity_list, three_m_yields):
            three_month_dict[maturity] = three_m_yield

        for maturity, eod_yield in zip(maturity_list, eod_yields):
            eod_dict[maturity] = eod_yield

        curve_dict = {
            '6mo': six_month_dict,
            '3mo': three_month_dict,
            'eod': eod_dict,
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = curve_dict
            return output
        elif display == 'table':
            curve_df = pd.DataFrame.from_dict(curve_dict)
            curve_df.columns = curve_df.columns.str.upper()
            curve_df.index.name = 'Maturity'
            output = curve_df
            return output
        elif display == 'line':
            iso_country_dict = {
                        'AU': 'Australia',
                        'AT': 'Austria',
                        'BH': 'Bahrain',
                        'BD': 'Bangladesh',
                        'BE': 'Belgium',
                        'BR': 'Brazil',
                        'BG': 'Bulgaria',
                        'CA': 'Canada',
                        'CL': 'Chile',
                        'CN': 'China',
                        'CO': 'Colombia',
                        'CI': "Cote D'Ivoire",
                        'HR': 'Croatia',
                        'CY': 'Cyprus',
                        'CZ': 'Czech Republic',
                        'DK': 'Denmark',
                        'EG': 'Egypt',
                        'FI': 'Finland',
                        'FR': 'France',
                        'DE': 'Germany',
                        'GR': 'Greece',
                        'HK': 'Hong Kong',
                        'HU': 'Hungary',
                        'IS': 'Iceland',
                        'IN': 'India',
                        'ID': 'Indonesia',
                        'IE': 'Ireland',
                        'IL': 'Israel',
                        'IT': 'Italy',
                        'JP': 'Japan',
                        'KZ': 'Kazakhstan',
                        'KE': 'Kenya',
                        'LV': 'Latvia',
                        'LT': 'Lithuania',
                        'MY': 'Malaysia',
                        'MT': 'Malta',
                        'MU': 'Mauritius',
                        'MX': 'Mexico',
                        'MA': 'Morocco',
                        'NA': 'Namibia',
                        'NL': 'Netherlands',
                        'NZ': 'New Zealand',
                        'NG': 'Nigeria',
                        'NO': 'Norway',
                        'PK': 'Pakistan',
                        'PE': 'Peru',
                        'PH': 'Philippines',
                        'PL': 'Poland',
                        'PT': 'Portugal',
                        'QA': 'Qatar',
                        'RO': 'Romania',
                        'RU': 'Russia',
                        'RS': 'Serbia',
                        'SG': 'Singapore',
                        'SK': 'Slovakia',
                        'SI': 'Slovenia',
                        'ZA': 'South Africa',
                        'KR': 'South Korea',
                        'ES': 'Spain',
                        'LK': 'Sri Lanka',
                        'SE': 'Sweden',
                        'CH': 'Switzerland',
                        'TW': 'Taiwan',
                        'TH': 'Thailand',
                        'TR': 'Turkey',
                        'UG': 'Uganda',
                        'UA': 'Ukraine',
                        'GB': 'United Kingdom',
                        'US': 'United States',
                        'VN': 'Vietnam',
                        'ZM': 'Zambia'
                    }
            
            curve_df = pd.DataFrame.from_dict(curve_dict)
            curve_df.columns = curve_df.columns.str.upper()

            fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)

            mask = np.isfinite(curve_df['EOD'])

            if eod_line:
                ax.plot(curve_df.index[mask], curve_df['EOD'][mask], marker = 'o', markersize=3, markerfacecolor='white', color='#354169', label='Last Close')

            if three_month_line:
                ax.plot(curve_df.index[mask], curve_df['3MO'][mask], marker = 'o', markersize=3, markerfacecolor='white', color='#c76861', label='3 Months Ago')

            if six_month_line:
                ax.plot(curve_df.index[mask], curve_df['6MO'][mask], marker = 'o', markersize=3, markerfacecolor='white', color='#5baecf', label='6 Months Ago')

            ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1])

            if eod_line:
                ax.fill_between(curve_df.index[mask], ax.get_ylim()[0], curve_df['EOD'][mask], color = '#354169', alpha = 0.1)

            ax.set_title(f'{iso_country_dict[country]} Yield Curve', fontsize=6.5, loc='left', pad=4, fontname='Arial', weight='bold')

            if (eod_line + three_month_line + six_month_line) >= 2:
                ax.legend(fontsize=6, frameon=False, facecolor=None, borderaxespad=1.2)

            #PLOT AESTHETICS---------------------------------------------------------------
            ax.set_facecolor('#E6F2FA') #BACKGROUND COLOR

            for spine in ax.spines.values(): # SPINES AKA EDGES
                spine.set_visible(True)            # ensure visibility
                spine.set_edgecolor('#7A7A7A')    # gray color
                spine.set_linewidth(0.15)          # adjust thickness

            ax.minorticks_on() #need to turn on minor ticks to plot minor grid lines
            ax.tick_params(which="minor", axis='both', direction='out', color='white', width=0) #minor ticks invisible
            ax.tick_params(which="major", axis='both', direction='out', width=1, zorder=3) #major ticks

            ax.grid(which='major', color='#FFFFFF', linestyle='-', linewidth=0.8, zorder=0) #major grid lines
            ax.grid(which='minor', color='#FFFFFF', linestyle='--', linewidth=0.4, zorder=0) #minor grid lines

            ax.yaxis.tick_right()            # ticks appear on the right
            ax.yaxis.set_label_position("right")  # y-axis label moves to the right

            for label in ax.get_xticklabels() + ax.get_yticklabels(): #sets all label fonts to 7 and Arial
                label.set_fontsize(7)
                label.set_fontname('Arial')

            ax.set_axisbelow(True) #making the grid and everything below the actual data line
            #------------------------------------------------------------------------------

            plt.show()
#------------------------------------------------------------------------------------------
    def eod(self, display: str = 'json', maturity: str = '10y', country: str = 'US'): 
        valid_params = {'valid_display': ['json', 'pretty'],
                        'valid_maturity': ['6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y'],
                        'valid_country' : ['AU', 'AT', 'BH', 'BD', 'BE', 'BR', 'BG', 'CA', 'CL', 'CN', 'CO', 'CI', 'HR', 'CY', 'CZ', 'DK', 'EG', 'FI', 'FR', 'DE', 'GR', 'HK', 'HU', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JP', 'KZ', 'KE', 'LV', 'LT', 'MY', 'MT', 'MU', 'MX', 'MA', 'NA', 'NL', 'NZ', 'NG', 'NO', 'PK', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU', 'RS', 'SG', 'SK', 'SI', 'ZA', 'KR', 'ES', 'LK', 'SE', 'CH', 'TW', 'TH', 'TR', 'UG', 'UA', 'GB', 'US', 'VN', 'ZM']}
        
        params = {'display': display,
                  'maturity': maturity,
                  'country': country}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        yield_df = self.sovereign_timeseries(display = 'table', period = '6mo', interval = '1d', data = 'close', maturity=maturity, country=country)
        #----------------------------------------------------------------------------------

        iso_country_dict = {
            'AU': 'Australia',
            'AT': 'Austria',
            'BH': 'Bahrain',
            'BD': 'Bangladesh',
            'BE': 'Belgium',
            'BR': 'Brazil',
            'BG': 'Bulgaria',
            'CA': 'Canada',
            'CL': 'Chile',
            'CN': 'China',
            'CO': 'Colombia',
            'CI': "Cote D'Ivoire",
            'HR': 'Croatia',
            'CY': 'Cyprus',
            'CZ': 'Czech Republic',
            'DK': 'Denmark',
            'EG': 'Egypt',
            'FI': 'Finland',
            'FR': 'France',
            'DE': 'Germany',
            'GR': 'Greece',
            'HK': 'Hong Kong',
            'HU': 'Hungary',
            'IS': 'Iceland',
            'IN': 'India',
            'ID': 'Indonesia',
            'IE': 'Ireland',
            'IL': 'Israel',
            'IT': 'Italy',
            'JP': 'Japan',
            'KZ': 'Kazakhstan',
            'KE': 'Kenya',
            'LV': 'Latvia',
            'LT': 'Lithuania',
            'MY': 'Malaysia',
            'MT': 'Malta',
            'MU': 'Mauritius',
            'MX': 'Mexico',
            'MA': 'Morocco',
            'NA': 'Namibia',
            'NL': 'Netherlands',
            'NZ': 'New Zealand',
            'NG': 'Nigeria',
            'NO': 'Norway',
            'PK': 'Pakistan',
            'PE': 'Peru',
            'PH': 'Philippines',
            'PL': 'Poland',
            'PT': 'Portugal',
            'QA': 'Qatar',
            'RO': 'Romania',
            'RU': 'Russia',
            'RS': 'Serbia',
            'SG': 'Singapore',
            'SK': 'Slovakia',
            'SI': 'Slovenia',
            'ZA': 'South Africa',
            'KR': 'South Korea',
            'ES': 'Spain',
            'LK': 'Sri Lanka',
            'SE': 'Sweden',
            'CH': 'Switzerland',
            'TW': 'Taiwan',
            'TH': 'Thailand',
            'TR': 'Turkey',
            'UG': 'Uganda',
            'UA': 'Ukraine',
            'GB': 'United Kingdom',
            'US': 'United States',
            'VN': 'Vietnam',
            'ZM': 'Zambia'
        }

        maturity_dict = {
            '6mo': '6M',
            '1y': '1Y',
            '2y': '2Y',
            '3y': '3Y',
            '5y': '5Y',
            '7y': '7Y',
            '10y': '10Y',
            '20y': '20Y',
            '30y': '30Y'
        }

        date = yield_df.index[-1].strftime('%Y-%m-%d')

        eod_figure = float(yield_df.iloc[-1])

        #JSON FORMAT DATA
        eod_data = {
            'country': iso_country_dict[country],
            'maturity': maturity.upper(),
            'date': date,
            'yield': eod_figure
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = eod_data
            return output
        if display == 'pretty':
            output = f''' COUNTRY - {eod_data['country']}
MATURITY - {eod_data['maturity']}
    DATE - {eod_data['date']}
   YIELD - {eod_data['yield']}'''
            print(output)
#------------------------------------------------------------------------------------------
    def bond_quote(self, display: str = 'json', maturity: str = '10y', country: str = 'US'): 
        valid_params = {'valid_display': ['json', 'pretty'],
                        'valid_maturity': ['6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y'],
                        'valid_country' : ['AU', 'AT', 'BH', 'BD', 'BE', 'BR', 'BG', 'CA', 'CL', 'CN', 'CO', 'CI', 'HR', 'CY', 'CZ', 'DK', 'EG', 'FI', 'FR', 'DE', 'GR', 'HK', 'HU', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JP', 'KZ', 'KE', 'LV', 'LT', 'MY', 'MT', 'MU', 'MX', 'MA', 'NA', 'NL', 'NZ', 'NG', 'NO', 'PK', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU', 'RS', 'SG', 'SK', 'SI', 'ZA', 'KR', 'ES', 'LK', 'SE', 'CH', 'TW', 'TH', 'TR', 'UG', 'UA', 'GB', 'US', 'VN', 'ZM']}
        
        params = {'display': display,
                  'maturity': maturity,
                  'country': country}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        if Config.fred_apikey is None:
            raise MissingConfigObject('Missing fred_apikey. Please set your FRED api key using the set_config() function.')
        
        #RAW DATA/OBSERVATIONS--------------------------------------------------------------
        yield_timeseries = self.sovereign_timeseries(display = 'table', period = '10y', interval = '1d', data = 'all', maturity=maturity, country=country)
        
        yield_eod = self.eod(display='json', maturity=maturity, country=country)['yield']

        current_year = pd.Timestamp.now().year 
        #-----------------------------------------------------------------------------------
        
        #DATES
        initial_dates = [
            date.today() - relativedelta(years=5),
            date.today() - relativedelta(years=1),
            date.today() - relativedelta(months=6),
            date.today() - relativedelta(months=1)
        ]

        initial_dates = [pd.Timestamp(d) for d in initial_dates]

        f_dates = []

        for d in initial_dates:
            while d not in yield_timeseries.index.tolist():
                d = d + relativedelta(days=1)
            f_dates.append(d)

        final_dates = {
            '5y' : f_dates[0],
            '1y' : f_dates[1],
            '6m' : f_dates[2],
            '1m' : f_dates[3],
        }
    
        #JSON FORMAT DATA
        quote_data = {
            'identifier': f'{country} {maturity.upper()} Bond Yield',
            'ttm': {
                'high': round(float(yield_timeseries.loc[final_dates['1y']:].max().max()),2),
                'low': round(float(yield_timeseries.loc[final_dates['1y']:].min().min()),2)
            },
            'percent change': {
                '5y': float((yield_eod/yield_timeseries[f'{country} {maturity.upper()} Close'].loc[final_dates['5y']]) - 1),
                '1y': float((yield_eod/yield_timeseries[f'{country} {maturity.upper()} Close'].loc[final_dates['1y']]) - 1),
                'ytd': float((yield_eod/yield_timeseries[f'{country} {maturity.upper()} Close'][yield_timeseries.index.year == current_year].iloc[0]) - 1),
                '6mo': float((yield_eod/yield_timeseries[f'{country} {maturity.upper()} Close'].loc[final_dates['6m']]) - 1),
                '1mo': float((yield_eod/yield_timeseries[f'{country} {maturity.upper()} Close'].loc[final_dates['1m']]) - 1),
                '5d': float((yield_eod/yield_timeseries[f'{country} {maturity.upper()} Close'].iloc[-5]) - 1)
            },
            '50d average yield': round(float(yield_timeseries[f'{country} {maturity.upper()} Close'].iloc[-50:].mean()),2),
            '200d average yield': round(float(yield_timeseries[f'{country} {maturity.upper()} Close'].iloc[-200:].mean()),2)
        }

        #PARAMETER - DISPLAY ===============================================================
        if display == 'json':
            output = quote_data
            return output
        elif display == 'pretty':
            output = f'''
{quote_data['identifier']} Quote

TTM HIGH/LOW----------------------------
         HIGH --  {quote_data['ttm']['high']}
          LOW --  {quote_data['ttm']['low']}
PERCENT CHANGE--------------------------
       5 YEAR -- {' ' if pd.isna(quote_data['percent change']['5y']) or quote_data['percent change']['5y']>0 else ''}{round(quote_data['percent change']['5y'] * 100,2)}%
       1 YEAR -- {' ' if pd.isna(quote_data['percent change']['1y']) or quote_data['percent change']['1y']>0 else ''}{round(quote_data['percent change']['1y'] * 100,2)}%
          YTD -- {' ' if pd.isna(quote_data['percent change']['ytd']) or quote_data['percent change']['ytd']>0 else ''}{round(quote_data['percent change']['ytd'] * 100,2)}%
      6 MONTH -- {' ' if pd.isna(quote_data['percent change']['6mo']) or quote_data['percent change']['6mo']>0 else ''}{round(quote_data['percent change']['6mo'] * 100,2)}%
      1 MONTH -- {' ' if pd.isna(quote_data['percent change']['1mo']) or quote_data['percent change']['1mo']>0 else ''}{round(quote_data['percent change']['1mo'] * 100,2)}%
        5 DAY -- {' ' if pd.isna(quote_data['percent change']['5d']) or quote_data['percent change']['5d']>0 else ''}{round(quote_data['percent change']['5d'] * 100,2)}%
MOVING AVERAGES-------------------------
 50 DAY YIELD --  {round(quote_data['50d average yield'],2)}
200 DAY YIELD --  {round(quote_data['200d average yield'],2)}
'''
            print(output)
#------------------------------------------------------------------------------------------
    def US_HQM_corporate(self, display: str = 'table', maturity: str = '10y', period: str = '5y', show: str = True, save: str = False): 
        valid_params = {'valid_display': ['table', 'json', 'line', 'bar'],
                        'valid_maturity': ['6mo', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y'],
                        'valid_period' : ['6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        'valid_show' : [True, False],
                        'valid_save' : [True, False]}
        
        params = {'display': display,
                  'maturity': maturity,
                  'valid_period': period,
                  'show': show,
                  'save': save}

        for param_key, param_value, valid_param in zip(params.keys(), params.values(), valid_params.values()):
            if param_value not in valid_param:
                raise InvalidParameterError(f"Invalid {param_key} parameter '{param_value}'. "
                                            f"Please choose a valid parameter: {', '.join(valid_param)}")

        FRED_IDs = {
            '6mo': 'HQMCB6MT',
            '1y': 'HQMCB1YR',
            '2y': 'HQMCB2YR',
            '3y': 'HQMCB3YR',
            '5y': 'HQMCB5YR',
            '7y': 'HQMCB7YR',
            '10y': 'HQMCB10YR',
            '20y': 'HQMCB20YR',
            '30y': 'HQMCB30YR'
        }

        if Config.fred_apikey is None:
            raise MissingConfigObject('Missing fred_apikey. Please set your FRED api key using the set_config() function.')
        
        #RAW DATA/OBSERVATION--------------------------------------------------------------
        id = FRED_IDs[maturity]

        FRED_url = f'{Config.fred_baseurl}series/observations?series_id={id}&api_key={Config.fred_apikey}&file_type=json'
        FRED_yield = requests.get(FRED_url).json()
        yield_df = pd.DataFrame(FRED_yield['observations'])
        yield_df = yield_df.drop(columns=['realtime_start', 'realtime_end'])
        yield_df['date'] = pd.to_datetime(yield_df['date'])
        yield_df['value'] = pd.to_numeric(yield_df['value'], errors='coerce')
        yield_df = yield_df.set_index('date')
        yield_df.index.name = 'Date'
        yield_df = yield_df.rename(columns={'value': f'US HQM {maturity.upper()}'})

        current_year = pd.Timestamp.now().year
        #----------------------------------------------------------------------------------
        #DATES
        initial_dates = [
            date.today().replace(day=1) - relativedelta(months=6),
            date.today().replace(day=1) - relativedelta(years=1),
            date.today().replace(day=1) - relativedelta(years=2),
            date.today().replace(day=1) - relativedelta(years=5),
            date.today().replace(day=1) - relativedelta(years=10)
        ]

        initial_dates = [pd.Timestamp(d) for d in initial_dates]

        final_dates = {
            '6mo' : initial_dates[0],
            '1y' : initial_dates[1],
            '2y' : initial_dates[2],
            '5y' : initial_dates[3],
            '10y' : initial_dates[4],
        }
        
        #PARAMETER - PERIOD ================================================================  
        if period == 'max':
            yield_df = yield_df

        elif period == 'ytd':
            yield_df = yield_df[yield_df.index.year == current_year]

        else:
            yield_df = yield_df.loc[final_dates[period]:]

        #PARAMETER - DISPLAY ==============================================================
        if display == 'table':
            output = yield_df
            return output
        elif display == 'json':
            yield_df.index = yield_df.index.strftime('%Y-%m-%d')

            data_json_list = []
            for index, row in yield_df.iterrows():
                a = {
                    'Date': index,
                    f'{yield_df.columns[0]}': float(row[f'{yield_df.columns[0]}'])
                }
                data_json_list.append(a)
            output = data_json_list
            return output
        else:
            fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)

            if display == 'bar': ax.bar(yield_df.index, yield_df[yield_df.columns[0]], width=10)
            elif display == 'line':
                if period in ('6mo', '1y', '2y', '5y', 'ytd'):
                    ax.plot(yield_df.index, yield_df, marker = 'o', markersize=3, markerfacecolor='white')
                elif period in ('max', '10y'):
                    ax.plot(yield_df.index, yield_df)
            
            first_date = yield_df.index[0].strftime('%b %Y')
            last_date = yield_df.index[-1].strftime('%b %Y')

            ax.set_title(f'US High Quality Market {maturity.upper()} Bond Yields — ({first_date} - {last_date})', fontsize=6.5, loc='left', pad=4, fontname='Arial', weight='bold')

            #PLOT AESTHETICS---------------------------------------------------------------
            ax.set_facecolor('#E6F2FA') #BACKGROUND COLOR

            for spine in ax.spines.values(): # SPINES AKA EDGES
                spine.set_visible(True)            # ensure visibility
                spine.set_edgecolor('#7A7A7A')    # gray color
                spine.set_linewidth(0.15)          # adjust thickness

            ax.minorticks_on() #need to turn on minor ticks to plot minor grid lines
            ax.tick_params(which="minor", axis='both', direction='out', color='white', width=0) #minor ticks invisible
            ax.tick_params(which="major", axis='both', direction='out', width=1, zorder=3) #major ticks

            ax.grid(which='major', color='#FFFFFF', linestyle='-', linewidth=0.8, zorder=0) #major grid lines
            ax.grid(which='minor', color='#FFFFFF', linestyle='--', linewidth=0.4, zorder=0) #minor grid lines

            ax.yaxis.tick_right()            # ticks appear on the right
            ax.yaxis.set_label_position("right")  # y-axis label moves to the right

            for label in ax.get_xticklabels() + ax.get_yticklabels(): #sets all label fonts to 7 and Arial
                label.set_fontsize(7)
                label.set_fontname('Arial')

            ax.set_axisbelow(True) #making the grid and everything below the actual data line
            #SAVE--------------------------------------------------------------------------
            if save:
                plt.savefig(f'USHQM{maturity.upper()}_{yield_df.index[0].strftime('%b%Y')}_{yield_df.index[-1].strftime('%b%Y')}.png', dpi=300, bbox_inches='tight')

            #SHOW--------------------------------------------------------------------------
            if show:
                plt.show()
            elif show == False:
                plt.close(fig)
#------------------------------------------------------------------------------------------