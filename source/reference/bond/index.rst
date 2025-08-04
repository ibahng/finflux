Fixed Income - finflux.bond()
===============================

The ``bond()`` class does not require any input.

Functions
-----------

.. py:function:: nonUS_10Y_sovereign(country = None, period = '5y')

   :param country: The country for which data is requested; VALID VALUES: ``'KR'`` , ``'AT'`` , ``'CL'`` , ``'CZ'`` , ``'GR'`` , ``'FI'`` , ``'ZA'`` , ``'NL'`` , ``'SK'`` , ``'NZ'`` , ``'LU'`` , ``'PL'`` , ``'SI'`` , ``'CH'`` , ``'DE'`` , ``'CA'`` , ``'JP'`` , ``'DK'`` , ``'BE'`` , ``'FR'`` , ``'NO'`` , ``'PT'`` , ``'IT'`` , ``'GB'`` , ``'ES'`` , ``'IE'`` , ``'AU'`` , ``'SE'`` , ``'MX'`` , ``'HU'`` , ``'IS'``
   :type country: str
   
   :param period: The duration of the timeseries; VALID VALUES: ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'`` 
   :type period: str

   :return: A pandas DataFrame of the monthly timeseries of a country's 10 year soverign bond yield.
   :source: Federal Reserve Economic Data (Organization for Economic Co-operation and Development)


   
.. py:function:: US_treasury(maturity = '10y', period = '5y')

   :param maturity: The maturity of the Treasury bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str

   :param period: The duration of the timeseries; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'``
   :type period: str
   
   :return: A pandas DataFrame of the daily timeseries of a US Treasury bond
   :source: Federal Reserve Economic Data (Board of Governers of the Federal Reserve System)



.. py:function:: US_curve(display = 'graph')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'`` , ``'graph'``
   :type display: str
   
   :return: The US Treasury bond yield curve data, formatted as either a JSON output, a pandas DataFrame, or a matplotlib graph
   :source: Federal Reserve Economic Data (Board of Governers of the Federal Reserve System)



.. py:function:: US_eod(display = 'json', maturity = '10y')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :param maturity: The maturity of the Treasury bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str
   
   :return: A JSON- or string-formatted display of the specified Treasury bond's latest end-of-day yield.
   :source: Federal Reserve Economic Data (Board of Governers of the Federal Reserve System)



.. py:function:: US_quote(display = 'json', maturity = '10y')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'pretty'``
   :type display: str

   :param maturity: The maturity of the Treasury bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str
   
   :return: The specified Treasury bond's quote, including TTM high/low, percentage changes over various periods, and SMAs for yield, formatted as either JSON or a string.
   :source: Federal Reserve Economic Data (Board of Governers of the Federal Reserve System)



.. py:function:: US_HQM_corporate(maturity = '10y', period = '5y')

   :param maturity: The maturity of the Treasury bond; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'3y'`` , ``'5y'`` , ``'7y'`` , ``'10y'`` , ``'20y'`` , ``'30y'``
   :type maturity: str

   :param period: The duration of the timeseries; VALID VALUES: ``'6mo'`` , ``'1y'`` , ``'2y'`` , ``'5y'`` , ``'10y'`` , ``'ytd'`` , ``'max'``
   :type period: str
   
   :return: A pandas DataFrame of the monthly timeseries of the high quality market (A, AA, AAA credit ratings) corporate bond yield
   :source: Federal Reserve Economic Data (US Department of Treasury)