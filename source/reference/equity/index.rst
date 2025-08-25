Equity - finflux.equity()
=========================

Before accessing the ``equity()`` class functions, you must first assign a string-formatted ticker symbol to the class's ``ticker`` attribute.

.. code-block:: python

   import finflux as ff
   ff.equity('TICKER').example_function(param1 = 'param', ...)
   #NOTE: Only ticker symbols searchable via Yahoo Finance are supported

Functions
-----------

.. py:function:: timeseries(display = 'table', period = '5y', start = None, end = None, interval = '1d', data = 'all', calculation = 'price', round = True, show = True, save = False)

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'`` , ``'line'``
   :type display: str

   :param period: The duration of the timeseries (used if **start** and **end** parameters are not provided); VALID VALUES: ``'1mo'`` , ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
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

   :param show: Display the chart as an output if ``display == 'line'``; VALID VALUES: ``True`` , ``False``
   :type show: bool

   :param save: Download the figure as a png if ``display == 'line'``; VALID VALUES: ``True`` , ``False``
   :type save: bool

   :return: A pandas DataFrame, row oriented JSON formatted output, or simple matplotlib graph of a timeseries OHLC price and volume data for the specified equity.
   :source: Yahoo Finance (yfinance)



.. py:function:: equity_candle(period = '6mo', start = None, end = None, interval = '1d', sma = None, volume = True, bollinger = None, o_label = True, h_label = True, l_label = True, c_label = True, legend = False, title = True, show = True, save = False)

   :param period: The duration of the chart (used if **start** and **end** parameters are not provided); VALID VALUES: ``'1mo'`` , ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :param start: Optional start date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type start: None or str

   :param end: Optional end date in ``'YYYY-MM-DD'`` format. Overrides **period** parameter if both **start** and **end** parameters are set.
   :type end: None or str

   :param interval: Candlestick frequency; VALID VALUES: ``'1d'`` , ``'1wk'`` , ``'1mo'``
   :type interval: str

   :param sma: Optional standard moving average line(s) generation (``len(sma)`` capped at 5); VALID VALUES: ``None`` , ``list of int >=10 and <=300``
   :type sma: None or list

   :param volume: Optional volume chart; VALID VALUES: ``True`` , ``False``
   :type volume: bool

   :param bollinger: Optional bollinger band standard deviation range(s) generation (``len(bollinger)`` must equal ``len(sma)``); VALID VALUES: ``None`` or ``list of int/float >=0.1 and <=3.0``
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

   :param show: Display the chart as an output; VALID VALUES: ``True`` , ``False``
   :type show: bool

   :param save: Download the figure as a png; VALID VALUES: ``True`` , ``False``
   :type save: bool

   :return: A matplotlib OHLC candlestick chart figure for the specified equity
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
   :source: Yahoo Finance (yfinance), Twelve Data



.. py:function:: equity_quote(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: The specified equity’s stock quote, including EOD OHLCV figures, TTM high/low, percentage changes over various periods, and SMAs for price and volume, formatted as either JSON or a string.
   :source: Yahoo Finance (yfinance)



.. py:function:: info(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: An overview of the specified equity's descriptive metadata, formatted as either JSON or a string.
   :source: Yahoo Finance (yfinance), US Securities and Exchange Commission



.. py:function:: filings(form = None)

   :param form: Specifies the form (e.g., ``'10-K'`` or ``'8-K'``) to retrieve - REQUIRED
   :type form: str

   :return: A pandas DataFrame of the metadata of the specified equity's ``form`` within "at least one year's of filing or to 1,000 (whichever is more) of the most recent filings" (`SEC EDGAR APIs <https://www.sec.gov/search-filings/edgar-application-programming-interfaces>`_)
   :source: US Securities and Exchange Commission



.. py:function:: analyst_estimates(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: The specified equity's earnings, revenue, growth, and price estimates for the current/next quarter and year, formatted as either JSON or a string.
   :source: Yahoo Finance (yfinance)



.. py:function:: dividend(display = 'json', period = '5y', show = True, save = False)

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'`` , ``'line'`` , ``'bar'``
   :type display: str

   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :param show: Display the chart as an output if ``display in ('line', 'bar')``; VALID VALUES: ``True`` , ``False``
   :type show: bool

   :param save: Download the figure as a png if ``display in ('line', 'bar')``; VALID VALUES: ``True`` , ``False``
   :type save: bool

   :return: A pandas DataFrame, JSON-formatted output, or simple matplotlib graph of the timeseries dividend data for the specified equity.
   :source: Yahoo Finance (yfinance)



.. py:function:: split(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :return: A pandas DataFrame or JSON-formatted output of the timeseries stock split data for the specified equity.
   :source: Yahoo Finance (yfinance)



.. py:function:: stats(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :return: A comprehensive overview of the specified equity’s valuation, profitability, growth, liquidity, leverage, efficiency, and cash flow metrics across the past four fiscal years and the most recent period.
   :source: Yahoo Finance (yfinance)



.. py:function:: eps(display = 'json')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type display: str

   :return: A pandas DataFrame or row oriented JSON formatted output of the timeseries eps data for the past 10 or 11 quarters of the specified equity.
   :source: Yahoo Finance (yfinance)