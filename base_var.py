def set_apikeys(td=None, av=None, cg=None, fmp=None, fred=None):
    global td_apikey, av_apikey, cg_apikey, fmp_apikey, fred_apikey
    td_apikey   = f'{td}'
    av_apikey   = f'{av}'
    cg_apikey   = f'{cg}'
    fmp_apikey  = f'{fmp}'
    fred_apikey = f'{fred}'

td_baseurl   = 'https://api.twelvedata.com/'
av_baseurl   = 'https://www.alphavantage.co/query?function='
cg_baseurl   = 'https://pro-api.coingecko.com/api/v3/'
fmp_baseurl  = 'https://financialmodelingprep.com/api/'
imf_baseurl  = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
fred_baseurl = 'https://api.stlouisfed.org/fred/'
sec_baseurl  = 'https://www.sec.gov/'
