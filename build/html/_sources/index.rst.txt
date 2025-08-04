.. finflux documentation master file, created by
   sphinx-quickstart on Sun Aug  3 11:41:36 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to finflux API!
==========================

.. admonition:: IMPORTANT LEGAL DISCLAIMERS

   ``finflux`` is a Python library that provides a unified interface to access publicly available financial data via first- and third-party APIs, including yfinance, Twelve Data, FRED, BLS, BEA, and SEC. This project is **not** affiliated with or endorsed by any of these providers. All data and trademarks remain the property of their respective owners.

   The library is provided “as is” without warranties of any kind. **No guarantees** are made regarding the accuracy, completeness, or reliability of the data retrieved. Users assume **full responsibility** for how they use the information and are solely responsible for complying with each provider’s terms of service and rate limits.

   By using ``finflux``, you agree that the authors and contributors are **not** liable for any damages resulting from its use.

Introduction
------------

``finflux`` is a Python library that aggregates financial and market data from multiple publicly available RESTful JSON APIs. It currently covers equities, bonds, and U.S. economic indicators, offering a consistent and lightweight way to access and work with this data using straightforward code.

``finflux`` leverages both first-party and third-party APIs sourced from the data providers listed below:

- `Yahoo Finance <https://finance.yahoo.com/>`__
- `Twelve Data <https://twelvedata.com/>`__
- `Securities and Exchange Commission (SEC) <https://www.sec.gov/>`__
- `Organization for Economic Co-operation and Development (OECD) <https://www.oecd.org/en.html>`__
- `Board of Governors of the Federal Reserve System <https://www.federalreserve.gov/>`__
- `U.S. Department of the Treasury <https://home.treasury.gov/>`__
- `Bureau of Economic Analysis (BEA) <https://www.bea.gov/>`__
- `Bureau of Labor Statistics (BLS) <https://www.bls.gov/>`__
- `U.S. Census Bureau <https://www.census.gov/>`__
- `National Association of REALTORS® (NAR) <https://www.nar.realtor/>`__
- `Freddie Mac <https://www.freddiemac.com/>`__
- `University of Michigan <https://umich.edu/>`__

Install
-------

.. code-block:: bash

    $ pip install finflux

Quick start
-----------

First, import the library.

.. code-block:: python

   import finflux as ff

Before using data retrieval functions, you must configure your API keys and email address for specific endpoints that require user identification. If a required identifier is missing when calling a function, a ``MissingConfigObject`` error will be raised.

Currently, functions that access Twelve Data, FRED, BEA, BLS, and SEC data require identifiers: API keys for all except the SEC, which requires an email address. Use the links below to obtain the necessary credentials for each provider.

- `Twelve Data <https://twelvedata.com/>`__
- `Federal Reserve Economic Data <https://fred.stlouisfed.org/docs/api/api_key.html>`__
- `Bureau of Economic Analysis <https://apps.bea.gov/api/signup/>`__
- `Bureau of Labor Statistics <https://data.bls.gov/registrationEngine/>`__

Once you have obtained all required credentials, configure your API keys and email address using the ``set_config`` function.

.. code-block:: python

   ff.set_config(
      td = 'your_twelve_data_api_key',
      email = 'example@example.com',
      fred = 'your_FRED_api_key',
      bea = 'your_BEA_api_key',
      bls = 'your_BLS_api_key',
   )

Use Case Examples
-----------------

EXAMPLE #1: Retrieving dataframe formatted annual income statement data in EUR in millions excluding units past the decimals for Apple Inc. (AAPL).

.. code-block:: python

   ff.equity('AAPL').statement(display='table', statement='income', currency='EUR', unit='million', decimal=False, interval='annual')

EXAMPLE #2: Retrieving dataframe formatted monthly timeseries of the US high quality market (A, AA, AAA credit ratings) 7 year maturity corporate bond yield for the past 10 years.

.. code-block:: python

   ff.bond().US_HQM_corporate(maturity='7y', period='10y')

.. toctree::
   :maxdepth: 1
   :titlesonly:

   reference/index
   development/index