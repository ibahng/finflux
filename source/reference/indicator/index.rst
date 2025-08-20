Indicator - finflux.indicator()
================================

The ``indicator()`` class does not require any input.

Functions
-----------

.. py:function:: gdp(type = 'n', period = '5y', figure = 'yoy')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param type: Type of gross domestic product; VALID VALUES: ``'n'`` (nominal) , ``'r'`` (real) , ``'n_pc'`` (nominal per capita) , ``'r_pc'`` (real per capita) , ``'d'`` (deflator)
   :type type: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'`` , 
   :type period: str

   :param figure: Data interpretation; VALID VALUES: ``'raw'`` , ``'yoy'`` , ``'pop'``
   :type figure: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a quarterly timeseries for specified US gross domestic product data
   :source: Bureau of Economic Analysis



.. py:function:: price_index(type = 'c', period = '5y', figure = 'yoy')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param type: Type of price index; VALID VALUES: ``'c'`` (consumer) , ``'p'`` (producer) , ``'cc'`` (core consumer) , ``'cp'`` (core producer)
   :type type: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'``
   :type period: str

   :param figure: Data interpretation; VALID VALUES: ``'raw'`` , ``'yoy'`` , ``'pop'``
   :type figure: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a monthly timeseries for specified US price index data
   :source: Bureau of Labor Statistics



.. py:function:: pce(type = 'raw', period = '5y', figure = 'yoy')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param type: Type of personal consumption expenditure; VALID VALUES: ``'raw'`` , ``'core'``
   :type type: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'``
   :type period: str

   :param figure: Data interpretation; VALID VALUES: ``'raw'`` , ``'yoy'`` , ``'pop'``
   :type figure: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a monthly timeseries for specified US personal consumption expenditure data
   :source: Bureau of Economic Analysis



.. py:function:: unemployment(type = 'U-3', period = '5y')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param type: Type of unemployment; VALID VALUES: ``'U-3'`` (unemployment) , ``'U-6'`` (underemployment) , ``'g=male'`` , ``'g=female'`` , ``'r=white'`` , ``'r=black'`` , ``'r=asian'`` , ``'r=hispanic'`` , ``'e<hs'`` (less than HS education) , ``'e=hs'`` , ``'e<bach'`` (less than bachelor's degree) , ``'e>=bach'`` 
   :type type: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'``
   :type period: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a monthly timeseries for specified US unemployment data
   :source: Bureau of Labor Statistics



.. py:function:: labor(type = 'participation', period = '5y')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param type: Type of labor metric; VALID VALUES: ``'participation'`` (Labor Force Participation Rate) , ``'payroll'`` (Nonfarm Payrolls) , ``'quits'`` (Quits Rate) , ``'openings'`` (Job Openings Rate) , ``'earnings'`` (Average Hourly Earnings) , ``'claims'`` (Initial Claims)
   :type type: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'``
   :type period: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a monthly or weekly timeseries for specified US labor metric data
   :source: Bureau of Labor Statistics



.. py:function:: sentiment(type = 'c_msci', period = '5y')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param type: Type of sentiment indicator; VALID VALUES: ``'c_mcsi'`` (University of Michigan Consumer Sentiment) , ``'c_mcie'`` (University of Michigan Consumer Inflation Expecations) , ``'c_oecd'`` (OECD Composite Consumer Confidence for US) , ``'b_oecd'`` (OECD Business Tendency Surveys Indicator for US Manufacturing)
   :type type: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'``
   :type period: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a monthly timeseries for specified US sentiment data
   :source: FRED (University of Michigan, Organization for Economic Co-operation and Development)



.. py:function:: fed_rate(interval = '1d', period = '5y')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param interval: Data frequency; VALID VALUES: ``'1d'`` , ``'1wk'`` , ``'2wk'`` , ``'1mo'``
   :type interval: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'``
   :type period: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a timeseries for the US federal funds rate
   :source: FRED (Board of Governors of the Federal Reserve System)



.. py:function:: housing(type = 'starts', period = '5y', figure = 'raw')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param type: Type of housing metric; VALID VALUES: ``'starts'`` (Housing Starts) , ``'nsales'`` (New Housing Sales) , ``'esales'`` (Existing Housing Sales) , ``'30y_rate'`` (30 Year Mortgage Rate) , ``'15y_rate'`` (15 Year Mortgage Rate)
   :type type: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'max'`` , ``'ytd'``
   :type period: str
   
   :param figure: Data interpretation; VALID VALUES: ``'raw'`` , ``'yoy'`` , ``'pop'``
   :type figure: str

   :return: A pandas DataFrame or row oriented JSON formatted output of a monthly or weekly timeseries for specified US housing metric data
   :source: FRED (US Census Bureau, National Association of Realtors, Freddie Mac)



.. py:function:: vix(period = '5y', start = None, end = None, interval = '1d', data = 'all')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param period: The duration of the timeseries (used if **start** and **end** parameters are not provided); VALID VALUES: ``'1mo'`` , ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :param start: Optional start date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type start: None or str

   :param end: Optional end date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type end: None or str

   :param interval: Data frequency; VALID VALUES: ``'1d'`` , ``'1wk'`` , ``'1mo'`` , ``'3mo'``
   :type interval: str

   :param data: Type of OHLC data to retrieve; VALID VALUES: ``'open'`` , ``'high'`` , ``'low'`` , ``'close'`` , ``'all'``
   :type data: str

   :return: A pandas DataFrame or row oriented JSON formatted output of timeseries data for the CBOE Volatility Index (VIX).
   :source: Yahoo Finance (yfinance)



.. py:function:: dollar_index(period = '5y', start = None, end = None, interval = '1d', data = 'all')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :param period: The duration of the timeseries (used if **start** and **end** parameters are not provided); VALID VALUES: ``'1mo'`` , ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :param start: Optional start date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type start: None or str

   :param end: Optional end date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type end: None or str

   :param interval: Data frequency; VALID VALUES: ``'1d'`` , ``'1wk'`` , ``'1mo'`` , ``'3mo'``
   :type interval: str

   :param data: Type of OHLC data to retrieve; VALID VALUES: ``'open'`` , ``'high'`` , ``'low'`` , ``'close'`` , ``'all'``
   :type data: str

   :return: A pandas DataFrame or row oriented JSON formatted output of timeseries data for the Dollar Index.
   :source: Yahoo Finance (yfinance)