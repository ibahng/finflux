class Config:
    td_apikey     = None
    av_apikey     = None
    cg_apikey     = None
    fmp_apikey    = None
    fred_apikey   = None
    email_address = None
    td_baseurl    = 'https://api.twelvedata.com/'
    av_baseurl    = 'https://www.alphavantage.co/query?function='
    cg_baseurl    = 'https://pro-api.coingecko.com/api/v3/'
    fmp_baseurl   = 'https://financialmodelingprep.com/api/'
    imf_baseurl   = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    fred_baseurl  = 'https://api.stlouisfed.org/fred/'
    sec_baseurl   = 'https://www.sec.gov/'

def set_config(td=None, av=None, cg=None, fmp=None, fred=None, email=None):
    Config.td_apikey     = td
    Config.av_apikey     = av
    Config.cg_apikey     = cg
    Config.fmp_apikey    = fmp
    Config.fred_apikey   = fred
    Config.email_address = email

