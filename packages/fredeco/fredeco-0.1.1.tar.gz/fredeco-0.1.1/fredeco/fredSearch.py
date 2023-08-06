def fred_list_series(fred_api,category_id=0):
    '''Find the series of a category
    
    This function returns a data frame with information related to all series for a specific category of data provided by FRED.

    Arguments
    --------
    fred_api: str
        Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.
    category_id: int
        The id for a category of series. The default value is 0, which is the root category.

        
    Example
    --------
    from fredeco.fredSearch import fred_list_series
    
    fred_list_series(fred_api, category_id=125)

    '''

    import pandas as pd
    import requests
    import json
    url="https://api.stlouisfed.org/fred/category/series?category_id="+str(category_id)+"&api_key="+str(fred_api)+"&file_type=json"
    url=str(url)
    r = requests.get(url)
    data = r.json()
    dl=pd.DataFrame(list(data.values())[7:][0])
    return dl

########################

def fred_info_series(fred_api,series):
    '''Find the information that describe an economic indicator.
    
    This function returns a dictionnary of information that describe a series, such as its title, if it is
    seasonally adjusted or not, the date of last update, the unit used as measure, the notes where data source may be found etc.

    Arguments
    --------
    fred_api: str
        Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.
    series: str 
        A time series ID.

        
    Example
    -------
    from fredeco.fredSearch import fred_info_series

    fred_info_series(series='GDP',fred_api=fred_api)

    '''
    
    import pandas as pd
    import requests
    import json
    url="https://api.stlouisfed.org/fred/series?series_id="+str(series)+"&api_key="+str(fred_api)+"&file_type=json"
    r = requests.get(url)
    data = r.json()
    return data

########################

def fred_search(fred_api,text):
    '''Search for series related to one or several keywords.

    This function returns a data frame of variables related to the keywords indicated by the user. 
    The data frame provide several information for the series provided, such as their id, title, frequency, units of measurement,
    some notes related to their respective source etc.

    Arguments
    --------
    fred_api: str
        Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.    Your registered FRED API keys. You can request an API key: https://fredaccount.stlouisfed.org/apikeys
    text    str
        The keywords to look for among the variables available in FRED data.

        
    Example
    ------- 
    from fredeco.fredSearch import fred_info_series

    fred_search(fred_api,text='Price index')
    
    '''
    import pandas as pd
    import requests
    import json
    text1='+'.join(text.split())
    url="https://api.stlouisfed.org/fred/series/search?search_text="+text1+"&api_key="+fred_api+"&file_type=json"
    r = requests.get(url)
    data = r.json()
    ds=pd.DataFrame(list(data.values())[7:][0])
    return ds


def fred_vintagedates(fred_api,series):
    '''Historical dates of release of new or revised data

    This function returns a list of historical dates of release of new or revised data for a specific series.

    Arguments
    --------
    fred_api: str
        Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.    Your registered FRED API keys. You can request an API key: https://fredaccount.stlouisfed.org/apikeys
    series: str 
        A time series ID.

        
    Example
    ------
    from fredeco.fredSearch import fred_vintagedates

    fredSearch.fred_vintagedates(fred_api,series='GDP')
    '''
    import pandas as pd
    import requests
    import json

    url="https://api.stlouisfed.org/fred/series/vintagedates?series_id="+series+"&api_key="+fred_api+"&file_type=json"
    r = requests.get(url)
    data = r.json()
    ds=list(data.values())[7:][0]
    return ds