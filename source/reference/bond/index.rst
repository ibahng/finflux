Fixed Income - finflux.bond()
===============================

The ``bond()`` class does not require any input.

Functions
-----------

.. py:function:: sovereign_timeseries(display = 'table', period = '5y', start = None, end = None, interval = '1d', data = 'all', maturity = '10y', country = 'US', show = True, save = False)

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'`` , ``'line'``
   :type display: str

   :param period: The duration of the timeseries; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :param start: Optional start date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type start: None or str

   :param end: Optional end date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type end: None or str

   :param interval: Data frequency; VALID VALUES: ``'1d'`` , ``'1wk'`` , ``'1mo'``
   :type interval: str

   :param data: Type of OHLCV data to retrieve; VALID VALUES: ``'open'`` , ``'high'`` , ``'low'`` , ``'close'`` , ``'all'``
   :type data: str

   :param maturity: The maturity of the sovereign bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str

   :param country: The country for which data is requested inputted as ISO 3166-1 alpha-2 codes; VALID VALUES: ``'AU'`` , ``'AT'`` , ``'BH'`` , ``'BD'`` , ``'BE'`` , ``'BR'`` , ``'BG'`` , ``'CA'`` , ``'CL'`` , ``'CN'`` , ``'CO'`` , ``'CI'`` , ``'HR'`` , ``'CY'`` , ``'CZ'`` , ``'DK'`` , ``'EG'`` , ``'FI'`` , ``'FR'`` , ``'DE'`` , ``'GR'`` , ``'HK'`` , ``'HU'`` , ``'IS'`` , ``'IN'`` , ``'ID'`` , ``'IE'`` , ``'IL'`` , ``'IT'`` , ``'JP'`` , ``'KZ'`` , ``'KE'`` , ``'LV'`` , ``'LT'`` , ``'MY'`` , ``'MT'`` , ``'MU'`` , ``'MX'`` , ``'MA'`` , ``'NA'`` , ``'NL'`` , ``'NZ'`` , ``'NG'`` , ``'NO'`` , ``'PK'`` , ``'PE'`` , ``'PH'`` , ``'PL'`` , ``'PT'`` , ``'QA'`` , ``'RO'`` , ``'RU'`` , ``'RS'`` , ``'SG'`` , ``'SK'`` , ``'SI'`` , ``'ZA'`` , ``'KR'`` , ``'ES'`` , ``'LK'`` , ``'SE'`` , ``'CH'`` , ``'TW'`` , ``'TH'`` , ``'TR'`` , ``'UG'`` , ``'UA'`` , ``'GB'`` , ``'US'`` , ``'VN'`` , ``'ZM'``
   :type country: str

   :param show: Display the chart as an output if ``display == 'line'``; VALID VALUES: ``True`` , ``False``
   :type show: bool

   :param save: Download the figure as a png if ``display == 'line'``; VALID VALUES: ``True`` , ``False``
   :type save: bool

   :return: A pandas DataFrame, row oriented JSON formatted output, or simple matplotlib graph of an OHLC timeseries of a sovereign bond.
   :source: Investing.com (investpy)


   
.. py:function:: bond_candle(period = '6mo', start = None, end = None, interval = '1d', sma = None, bollinger = None, o_label = True, h_label = True, l_label = True, c_label = True, legend = False, title = True, maturity = '10y', country = 'US', show = True, save = False)

   :param period: The duration of the timeseries; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :param start: Optional start date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type start: None or str

   :param end: Optional end date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type end: None or str

   :param interval: Data frequency; VALID VALUES: ``'1d'`` , ``'1wk'`` , ``'1mo'``
   :type interval: str

   :param sma: Optional standard moving average line(s) generation (``len(sma)`` capped at 5); VALID VALUES: ``None`` , ``list of int >=10 and <=300``
   :type sma: None or list

   :param bollinger: Optional bollinger band standard deviation range(s) generation (``len(bollinger)`` must equal ``len(sma)``); VALID VALUES: ``None`` or ``list of int/float >=0.1 and <=3.0 or None``
   :type bollinger: None or list

   :param o_label: Optional plot open price label; VALID VALUES: ``True`` , ``False``
   :type o_label: bool

   :param h_label: Optional plot high price label; VALID VALUES: ``True`` , ``False``
   :type h_label: bool

   :param l_label: Optional plot low price label; VALID VALUES: ``True`` , ``False``
   :type l_label: bool

   :param c_label: Optional plot close price label; VALID VALUES: ``True`` , ``False``
   :type c_label: bool

   :param legend: Optional legend; VALID VALUES: ``True`` , ``False``
   :type legend: bool

   :param title: Optional title; VALID VALUES: ``True`` , ``False``
   :type title: bool

   :param maturity: The maturity of the sovereign bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str

   :param country: The country for which data is requested inputted as ISO 3166-1 alpha-2 codes; VALID VALUES: ``'AU'`` , ``'AT'`` , ``'BH'`` , ``'BD'`` , ``'BE'`` , ``'BR'`` , ``'BG'`` , ``'CA'`` , ``'CL'`` , ``'CN'`` , ``'CO'`` , ``'CI'`` , ``'HR'`` , ``'CY'`` , ``'CZ'`` , ``'DK'`` , ``'EG'`` , ``'FI'`` , ``'FR'`` , ``'DE'`` , ``'GR'`` , ``'HK'`` , ``'HU'`` , ``'IS'`` , ``'IN'`` , ``'ID'`` , ``'IE'`` , ``'IL'`` , ``'IT'`` , ``'JP'`` , ``'KZ'`` , ``'KE'`` , ``'LV'`` , ``'LT'`` , ``'MY'`` , ``'MT'`` , ``'MU'`` , ``'MX'`` , ``'MA'`` , ``'NA'`` , ``'NL'`` , ``'NZ'`` , ``'NG'`` , ``'NO'`` , ``'PK'`` , ``'PE'`` , ``'PH'`` , ``'PL'`` , ``'PT'`` , ``'QA'`` , ``'RO'`` , ``'RU'`` , ``'RS'`` , ``'SG'`` , ``'SK'`` , ``'SI'`` , ``'ZA'`` , ``'KR'`` , ``'ES'`` , ``'LK'`` , ``'SE'`` , ``'CH'`` , ``'TW'`` , ``'TH'`` , ``'TR'`` , ``'UG'`` , ``'UA'`` , ``'GB'`` , ``'US'`` , ``'VN'`` , ``'ZM'``
   :type country: str

   :param show: Display the chart as an output; VALID VALUES: ``True`` , ``False``
   :type show: bool

   :param save: Download the figure as a png; VALID VALUES: ``True`` , ``False``
   :type save: bool
   
   :return: A matplotlib OHLC candlestick chart figure for the specified sovereign bond
   :source: Investing.com (investpy)



.. py:function:: curve(display = 'line', country = 'US', eod_line = True, three_month_line = True, six_month_line = True, show = True, save = False)

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'`` , ``'line'``
   :type display: str

   :param country: The country for which data is requested inputted as ISO 3166-1 alpha-2 codes; VALID VALUES: ``'AU'`` , ``'AT'`` , ``'BH'`` , ``'BD'`` , ``'BE'`` , ``'BR'`` , ``'BG'`` , ``'CA'`` , ``'CL'`` , ``'CN'`` , ``'CO'`` , ``'CI'`` , ``'HR'`` , ``'CY'`` , ``'CZ'`` , ``'DK'`` , ``'EG'`` , ``'FI'`` , ``'FR'`` , ``'DE'`` , ``'GR'`` , ``'HK'`` , ``'HU'`` , ``'IS'`` , ``'IN'`` , ``'ID'`` , ``'IE'`` , ``'IL'`` , ``'IT'`` , ``'JP'`` , ``'KZ'`` , ``'KE'`` , ``'LV'`` , ``'LT'`` , ``'MY'`` , ``'MT'`` , ``'MU'`` , ``'MX'`` , ``'MA'`` , ``'NA'`` , ``'NL'`` , ``'NZ'`` , ``'NG'`` , ``'NO'`` , ``'PK'`` , ``'PE'`` , ``'PH'`` , ``'PL'`` , ``'PT'`` , ``'QA'`` , ``'RO'`` , ``'RU'`` , ``'RS'`` , ``'SG'`` , ``'SK'`` , ``'SI'`` , ``'ZA'`` , ``'KR'`` , ``'ES'`` , ``'LK'`` , ``'SE'`` , ``'CH'`` , ``'TW'`` , ``'TH'`` , ``'TR'`` , ``'UG'`` , ``'UA'`` , ``'GB'`` , ``'US'`` , ``'VN'`` , ``'ZM'``
   :type country: str

   :param eod_line: Optional latest yield curve; VALID VALUES: ``True`` , ``False``
   :type eod_line: bool

   :param three_month_line: Optional yield curve 3 months ago; VALID VALUES: ``True`` , ``False``
   :type three_month_line: bool

   :param six_month_line: Optional yield curve 6 months ago; VALID VALUES: ``True`` , ``False``
   :type six_month_line: bool

   :param show: Display the chart as an output if ``display == 'line'``; VALID VALUES: ``True`` , ``False``
   :type show: bool

   :param save: Download the figure as a png if ``display == 'line'``; VALID VALUES: ``True`` , ``False``
   :type save: bool
   
   :return: The sovereign bond yield curve data, formatted as either a JSON output, a pandas DataFrame, or a matplotlib graph
   :source: Investing.com (investpy)



.. py:function:: eod(display = 'json', maturity = '10y', country = 'US')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :param maturity: The maturity of the sovereign bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str

   :param country: The country for which data is requested inputted as ISO 3166-1 alpha-2 codes; VALID VALUES: ``'AU'`` , ``'AT'`` , ``'BH'`` , ``'BD'`` , ``'BE'`` , ``'BR'`` , ``'BG'`` , ``'CA'`` , ``'CL'`` , ``'CN'`` , ``'CO'`` , ``'CI'`` , ``'HR'`` , ``'CY'`` , ``'CZ'`` , ``'DK'`` , ``'EG'`` , ``'FI'`` , ``'FR'`` , ``'DE'`` , ``'GR'`` , ``'HK'`` , ``'HU'`` , ``'IS'`` , ``'IN'`` , ``'ID'`` , ``'IE'`` , ``'IL'`` , ``'IT'`` , ``'JP'`` , ``'KZ'`` , ``'KE'`` , ``'LV'`` , ``'LT'`` , ``'MY'`` , ``'MT'`` , ``'MU'`` , ``'MX'`` , ``'MA'`` , ``'NA'`` , ``'NL'`` , ``'NZ'`` , ``'NG'`` , ``'NO'`` , ``'PK'`` , ``'PE'`` , ``'PH'`` , ``'PL'`` , ``'PT'`` , ``'QA'`` , ``'RO'`` , ``'RU'`` , ``'RS'`` , ``'SG'`` , ``'SK'`` , ``'SI'`` , ``'ZA'`` , ``'KR'`` , ``'ES'`` , ``'LK'`` , ``'SE'`` , ``'CH'`` , ``'TW'`` , ``'TH'`` , ``'TR'`` , ``'UG'`` , ``'UA'`` , ``'GB'`` , ``'US'`` , ``'VN'`` , ``'ZM'``
   :type country: str
   
   :return: A JSON- or string-formatted display of the specified sovereign bond's latest end-of-day yield.
   :source: Investing.com (investpy)



.. py:function:: bond_quote(display = 'json', maturity = '10y', country = 'US')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :param maturity: The maturity of the sovereign bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str

   :param country: The country for which data is requested inputted as ISO 3166-1 alpha-2 codes; VALID VALUES: ``'AU'`` , ``'AT'`` , ``'BH'`` , ``'BD'`` , ``'BE'`` , ``'BR'`` , ``'BG'`` , ``'CA'`` , ``'CL'`` , ``'CN'`` , ``'CO'`` , ``'CI'`` , ``'HR'`` , ``'CY'`` , ``'CZ'`` , ``'DK'`` , ``'EG'`` , ``'FI'`` , ``'FR'`` , ``'DE'`` , ``'GR'`` , ``'HK'`` , ``'HU'`` , ``'IS'`` , ``'IN'`` , ``'ID'`` , ``'IE'`` , ``'IL'`` , ``'IT'`` , ``'JP'`` , ``'KZ'`` , ``'KE'`` , ``'LV'`` , ``'LT'`` , ``'MY'`` , ``'MT'`` , ``'MU'`` , ``'MX'`` , ``'MA'`` , ``'NA'`` , ``'NL'`` , ``'NZ'`` , ``'NG'`` , ``'NO'`` , ``'PK'`` , ``'PE'`` , ``'PH'`` , ``'PL'`` , ``'PT'`` , ``'QA'`` , ``'RO'`` , ``'RU'`` , ``'RS'`` , ``'SG'`` , ``'SK'`` , ``'SI'`` , ``'ZA'`` , ``'KR'`` , ``'ES'`` , ``'LK'`` , ``'SE'`` , ``'CH'`` , ``'TW'`` , ``'TH'`` , ``'TR'`` , ``'UG'`` , ``'UA'`` , ``'GB'`` , ``'US'`` , ``'VN'`` , ``'ZM'``
   :type country: str
   
   :return: The specified sovereign bond's quote, including TTM high/low, percentage changes over various periods, and SMAs for yield, formatted as either JSON or a string.
   :source: Investing.com (investpy)



.. py:function:: US_HQM_corporate(display = 'table', maturity = '10y', period = '5y', show = True, save = False)

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'`` , ``'line'`` , ``'bar'``
   :type display: str

   :param maturity: The maturity of the US HQM corporate bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str

   :param period: The duration of the timeseries; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'``
   :type period: str

   :param show: Display the chart as an output if ``display in ('line', 'bar')``; VALID VALUES: ``True`` , ``False``
   :type show: bool

   :param save: Download the figure as a png if ``display in ('line', 'bar')``; VALID VALUES: ``True`` , ``False``
   :type save: bool
   
   :return: A pandas DataFrame or row oriented JSON formatted output of the monthly timeseries of the high quality market (A, AA, AAA credit ratings) corporate bond yield
   :source: Federal Reserve Economic Data (US Department of Treasury)