finflux.equity()
===================

.. py:function:: timeseries(period = '5y', start = None, end = None, interval = '1d', data = 'all', calculation = 'price', round = True)

   :param period: Duration of the timeseries (used if **start** and **end** parameters are not provided); VALID VALUES: ``'1mo'`` , ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :param start: Optional start date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type start: None or str

   :param end: Optional end date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type end: None or str

   :param interval: Data frequency; VALID VALUES: ``'1d'`` , ``'1wk'`` , ``'1mo'`` , ``'3mo'``
   :type interval: str

   :param data: Type of OHLCV data to retrieve; VALID VALUES: ``'open'`` , ``'high'`` , ``'low'`` , ``'close'`` , ``'volume'`` , ``'all'``
   :type data: str

   :param calculation: Data interpretation; VALID VALUES: ``'price'`` , ``'simple return'`` , ``'log return'``
   :type calculation: str

   :param round: Whether to round numerical values to 2 decimal places; VALID VALUES: ``True`` , ``False``
   :type round: bool

   :return: A pandas DataFrame with timeseries data for the specified equity.
   :source: Yahoo Finance (yfinance)



.. py:function:: realtime(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str
   
   :return: A JSON- or string-formatted display of the specified equity’s real-time stock price.
   :source: Twelve Data



.. py:function:: statement(display = 'json', statement = 'all', currency = None, unit = 'raw', decimal = False, interval = 'annual')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type tickers: str

   :param statement: Type of finanial statement to retrieve; VALID VALUES: ``'income'`` , ``'balance'`` , ``'cash'`` , ``'all'``
   :type tickers: str

   :param currency: Optional currency code (e.g., ``'EUR'`` or ``'KRW'``) for value conversion.
   :type tickers: None or str

   :param unit: Numerical unit format; VALID VALUES: ``'thousand'`` , ``'million'`` , ``'raw'``
   :type tickers: str

   :param decimal: Whether to return values with decimal precision; VALID VALUES: ``True`` , ``False``
   :type tickers: bool

   :param interval: Reporting frequency; VALID VALUES: ``'annual'`` , ``'quarter'``
   :type tickers: str

   :return: The specified equity’s financial statement data for the four most recent periods, formatted as either JSON or a pandas DataFrame.
   :source: Yahoo Finance (yfinance)



.. py:function:: quote(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: DataFrame or None
   :source: Yahoo Finance (yfinance)



.. py:function:: info(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: DataFrame or None
   :source: Yahoo Finance (yfinance)



.. py:function:: filings(form = None)

   :param form: 
   :type form: str

   :return: DataFrame or None
   :source: US Securities and Exchange Commission



.. py:function:: analyst_estimates(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: DataFrame or None
   :source: Yahoo Finance (yfinance)



.. py:function:: dividend(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :return: DataFrame or None
   :source: Yahoo Finance (yfinance)



.. py:function:: split(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :return: DataFrame or None
   :source: Yahoo Finance (yfinance)



.. py:function:: stats(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: DataFrame or None
   :source: Yahoo Finance (yfinance)
