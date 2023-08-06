from fredeco.fredSearch import fred_info_series, fred_list_series


def fred_series(series,fred_api,frequency='a',starttime='1776-07-04',endtime='9999-12-31',transform='lin'):
    '''Retreive and economic indicator from FRED® API

    Arguments
    ----------
    series: str 
        A time series ID, such as GDP.
    fred_api: str
    Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.
    frequency: str
       The frequency of data. The default value is 'a' for annual data; 'q' is for quarterly data; 'm' is for monthly data
    starttime: str
        The first date, as a string, of the time series data to retrieve. The default value is '1776-07-04'.
    endtime: str
        The last date, as a string, of the time series data to retrieve. The default value is '9999-12-31'.
    transform: str

    Example
    -------
    from fredeco.fredData import fred_series

    fred_series(series='GDP',fred_api='4e5rty8wfr')

   '''
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import requests
    import json
    url='https://api.stlouisfed.org/fred/series/observations?series_id='+str(series)+'&output_type=1'+'&frequency='+str(frequency)+'&units='+str(transform)+'&observation_start='+str(starttime)+'&observation_end='+str(endtime)+'&api_key='+str(fred_api)+'&file_type=json'
    
    try:
        r = requests.get(url)
        data = r.json()
        dat=pd.DataFrame([i for i in data.values()][12])
        dat=dat[['date','value']]
        dat.columns=['Dates',series]
        dat=dat.set_index('Dates')
    
        ####
        def to_float(x):  # Since missing values are strings, I convert to float 
            y=[]
            for i in x:
                try:
                    y.append(float(i))      # convert string values to float    
                except:
                    y.append(np.nan)        # convert strings related to missing data to NAN
            return y 
        z=[]
        for i in dat.columns:
            z.append(to_float(dat[i]))
            #####
        dat2=pd.DataFrame(z).transpose()   # build a data frame with the lists of float data
        dat2.index=dat.index;dat2.columns=dat.columns
        return dat2
        
    except IndexError:
        raise IndexError('At least, one of the arguments of the function have an inappropriate value. This is the case, for example, when the FRED® ID is misspelled.')

##############################################

def fred_multi_series(series,fred_api,frequency='a',starttime='1776-07-04',endtime='9999-12-31',transform='lin'):
    """Retrieve data for several economic indicators from FRED® API.

    This method return a data frame of several variables.

    Arguments
    ----------
    fred_api: str
        Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.
    series: str 
        A time series ID, such as GDP.
    frequency: str
       The frequency of data. The default value is 'a' for annual data; 'q' is for quarterly data; 'm' is for monthly data
    starttime: str
        The first date, as a string, of the time series data to retrieve. The default value is '1776-07-04'.
    endtime: str
        The last date, as a string, of the time series data to retrieve. The default value is '9999-12-31'.
    transform: str   


    Example
    -------
    from fredeco.fredData import fred_multi_series

    fred_multi_series(series=['GDP','GDPCA'],fred_api='4e5rty8wfr')

    """


    import pandas as pd
    dat=pd.DataFrame()
    try:

        i=0
        while i<len(series):
            y=fred_series(series=series[i],fred_api=fred_api, frequency=frequency, starttime=starttime, endtime=endtime,transform=transform)
            dat[series[i]]=y
            i=i+1
        return dat
    except IndexError:
        raise IndexError('At least, one of the arguments of the function have an inappropriate value. This is the case, for example, when the FRED® ID is misspelled.')

##########################################
############
def units(data):
    '''Unit of each series of data frame of FRED® data.

    This function returns a list
    
    Arguments
    --------
    fred_api: str
        Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.
    data: data frame
        a data frame of indicators retreived from FRED®. All columns names should be FRED® indicators IDs.

    Example
    --------
    from fredeco.fredData import units

    units(fred_api='4e5rty8wfr',df)

    '''
    
    u=[list((fred_info_series(series=i,fred_api=fred_api)).values())[2][0]['units'] for i in data.columns.tolist()]
    return u



def explore(fred_api,data):
    '''Explore some key statistics of a data frame of indicators retreived from FRED®. 

    This function returns a data frame with some information related to each economic indicator of the data frame x. 
    Most of the information provided are statistics calculated by the function for each one of the indicators.
    All columns names should be FRED® indicators IDs.
    
    Arguments
    --------
    fred_api: str
        Your registered FRED API keys. You can use the function fredKey.request_api_key() to request an API key on the FRED website.
    x: data frame
        a data frame of indicators retreived from FRED®. All columns names should be FRED® indicators IDs.

    Example
    -------
    from fredeco.fredData import explore

    explore(fred_api='4e5rty8wfr',df)  

    '''
    import pandas as pd
    import numpy as np
    import sys
    def cv(x):
        return np.std(x,axis=0)/np.mean(x,axis=0)
    try:
        des=pd.DataFrame({'Units':units(data),'N':data.count(),'Mean':data.mean(),'Median':data.median(),'Std':data.std(),'Min':data.min(),
            'Max':data.max(),'CV':cv(data),'25% quantile':data.quantile(q=0.25).tolist(),'50% quantile':data.quantile(q=0.5).tolist(),
            '75% quantile':data.quantile(q=0.75).tolist(),'skewness':data.skew(),'kurtosis':data.kurt()}).transpose()
        return des
    except IndexError as e:
        raise IndexError('Check if all columns names of data are FRED® ID. At least one of them maybe misspelled.')