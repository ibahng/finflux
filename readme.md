<!--README.md files serve as the main landing page on this directory's github repository. It is the first thing that a viewer sees when he or she enters the github repo.

-->
# FinFlux API

`finflux` offers financial and market data retrieval through multiple publicly available free REST JSON API endpoints found online in one aggregate Python library, currently covering equities, bonds, and US economic indicators.

`finflux` utilizes both first-party and third-party APIs connected to the sources listed below.
- Yahoo Finance
- Twelve Data
- Securities and Exchange Commission (SEC)
- Organization for Economic Co-operation and Development (OECD)
- Board of Governors of the Federal Reserve System
- U.S. Department of the Treasury
- Bureau of Economic Analysis (BEA)
- Bureau of Labor Statistics (BLS)
- U.S. Census Bureau
- National Association of REALTORS® (NAR)
- Freddie Mac
- University of Michigan

## Installation and Setup

First, install `finflux` from PyPi using `pip` and import the library using `import`

```bash
pip install finflux
```

```python
import finflux as ff
```

Before accessing data retrieval functions, you must set your API keys and email address to use certain functions within the library that require an identifier. If no API key or email address is found when needed, a `MissingConfigObject` error will be raised.

Currently, functions utilizing Twelve Data, SEC, FRED, BEA, and BLS APIs all require identifiers in the form of API keys (with the exception of the SEC, requiring an email address instead). Use the links below to retrieve API keys for each source.
- [Twelve Data](https://twelvedata.com/)
- [Federal Reserve Economic Data](https://fred.stlouisfed.org/docs/api/api_key.html)
- [Bureau of Economic Analysis](https://apps.bea.gov/api/signup/)
- [Bureau of Labor Statistics](https://data.bls.gov/registrationEngine/)

After gaining access to all API keys pertaining to data of your choice, input the identifier strings through the `set_config` function.

```
fin.set_config(
    td = 'your_twelve_data_api_key',
    email = 'example@example.com',
    fred = 'your_FRED_api_key',
    bea = 'your_BEA_api_key',
    bls = 'your_BLS_api_key'
)
```

## Library Components (Classes and Methods)

- `finflux.equity('EQUITY_TICKER')`
    - `timeseries()`, `realtime()`, `statement()`, `quote()`, `info()`, `filings()`, `analyst_estimates()`, `dividend()`, `split()`, `stats()`
- `finflux.bond()`
    - `nonUS_10Y_sovereign()`, `US_treasury()`, `US_curve()`, `US_eod()`, `US_quote()`, `US_HQM_corporate()`
- `finflux.US_indic()`: 
    - `gdp()`, `price_index()`, `pce()`, `unemployment()`, `labor()`, `sentiment()`, `fed_rate()`, `housing()`
- `finflux.top()`: 
    - `gainer()`, `loser()`, `active()`, `cap()`

EXAMPLE #1: Retrieving dataframe formatted annual income statement data in EUR in millions excluding units past the decimals for Apple Inc. (AAPL).

```python
ff.equity('AAPL').statement(display='table', statement='income', currency='EUR', unit='million', decimal=False, interval='annual')
```

EXAMPLE #2: Retrieving dataframe formatted monthly timeseries of the US high quality market (A, AA, AAA ratings) 7 year maturity corporate bond yield for the past 10 years.

```python
ff.bond().US_HQM_corporate(maturity='7y', period='10y')
```

EXAMPLE #3: Retrieving dataframe formatted monthly timeseries of the Michigan Consumer Sentiment Index for the past 2 years

```python
ff.indicator().sentiment(type='c_mcsi', period='2y')
```

EXAMPLE #4: Retrieving json formatted top 10 stock price gainers in the healthcare sector

```python
ff.top().gainer(display='json', sector='healthcare')
```