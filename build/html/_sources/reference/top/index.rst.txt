Top Performers - finflux.top()
==============================

The ``top()`` class does not require any prior input.

Other commets about different parameters

Functions
-----------

.. py:function:: gainer(display = 'json', sector = 'all')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type type: str

   :param sector: Sector of interest; VALID VALUES: ``'all'`` , ``'basic materials'`` , ``'communication services'`` , ``'consumer cyclical'`` , ``'consumer defensive'`` , ``'energy'`` , ``'financial services'`` , ``'healthcare'`` , ``'industrials'`` , ``'real estate'`` , ``'technology'`` , ``'utilities'``
   :type period: str

   :return: A JSON-formatted output or pandas DataFrame listing the equities with the highest percentage price appreciation from the last trading day.
   :source: Yahoo Finance (yfinance)



.. py:function:: loser(display = 'json', sector = 'all')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type type: str

   :param sector: Sector of interest; VALID VALUES: ``'all'`` , ``'basic materials'`` , ``'communication services'`` , ``'consumer cyclical'`` , ``'consumer defensive'`` , ``'energy'`` , ``'financial services'`` , ``'healthcare'`` , ``'industrials'`` , ``'real estate'`` , ``'technology'`` , ``'utilities'``
   :type period: str

   :return: A JSON-formatted output or pandas DataFrame listing the equities with the highest percentage price depreciation from the last trading day.
   :source: Yahoo Finance (yfinance)



.. py:function:: active(display = 'json', sector = 'all')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type type: str

   :param sector: Sector of interest; VALID VALUES: ``'all'`` , ``'basic materials'`` , ``'communication services'`` , ``'consumer cyclical'`` , ``'consumer defensive'`` , ``'energy'`` , ``'financial services'`` , ``'healthcare'`` , ``'industrials'`` , ``'real estate'`` , ``'technology'`` , ``'utilities'``
   :type period: str

   :return: A JSON-formatted output or pandas DataFrame listing the equities with the highest trading volume from the last trading day.
   :source: Yahoo Finance (yfinance)



.. py:function:: cap(display = 'json', sector = 'all')

   :param display: Specifies the output format; VALID VALUES: ``'json'`` , ``'table'``
   :type type: str

   :param sector: Sector of interest; VALID VALUES: ``'all'`` , ``'basic materials'`` , ``'communication services'`` , ``'consumer cyclical'`` , ``'consumer defensive'`` , ``'energy'`` , ``'financial services'`` , ``'healthcare'`` , ``'industrials'`` , ``'real estate'`` , ``'technology'`` , ``'utilities'``
   :type period: str

   :return: A JSON-formatted output or pandas DataFrame listing the equities with the highest market capitalizations from the last trading day.
   :source: Yahoo Finance (yfinance)