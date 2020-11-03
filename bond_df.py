from pyvalet import ValetInterpreter
import requests
import pandas as pd
from datetime import datetime as dt
import re
vi = ValetInterpreter()

# vi = ValetInterpreter()
# df_series, df = vi.get_series_observations("BD.CDN.2YR.DQ.YLD", response_format='csv')
# print(df)


# BOC/V39055    Government of Canada benchmark bond yields - 10 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.10YR.DQ.YLD
# BOC/V39051    Government of Canada benchmark bond yields - 2 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.2YR.DQ.YLD
# BOC/V39052    Government of Canada benchmark bond yields - 3 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.3YR.DQ.YLD
# BOC/V39053    Government of Canada benchmark bond yields - 5 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.5YR.DQ.YLD
# BOC/V39054    Government of Canada benchmark bond yields - 7 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.7YR.DQ.YLD
# BOC/V39056    Government of Canada benchmark bond yields - long-term    daily https://www.bankofcanada.ca/valet/series/BD.CDN.LONG.DQ.YLD

links = [
         'BD.CDN.2YR.DQ.YLD',
         'BD.CDN.3YR.DQ.YLD',
         'BD.CDN.5YR.DQ.YLD',
         'BD.CDN.7YR.DQ.YLD',
         'BD.CDN.10YR.DQ.YLD',
         'BD.CDN.LONG.DQ.YLD']
bond_names = {
    'V39051': 'two year bond',
    'V39052': 'three year bond',
    'V39053': 'five year bond',
    'V39054': 'seven year bond',
    'V39055': 'ten year bond',
    'V39056': 'long term bond'
}
bond_names2 = {
    '2': 'two year bond',
    '3': 'three year bond',
    '5': 'five year bond',
    '7': 'seven year bond',
    '1': 'ten year bond',
    'L': 'long term bond'
}
def fix_date(date):
    # print(date)
    # print(type(date))
    # start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
    # start_date_string = start_date.strftime('%B %d, %Y')
    # timestamp.dt.strftime('%Y-%m-%d')
    if isinstance(date,str):
        return date
    date = date.to_pydatetime(date)
    date = str(date)[:10]
    # date = dt.strptime(re.split('T| ', date)[0], '%Y-%m-%d')

    # date = dt.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
    # date = date.strftime('%B %d, %Y')
    return date

def get_df(link):
    # print(vi.series_list())
    df_series, df = vi.get_series_observations(link,response_format='csv')
    # print(df)
    df.columns = ['Date','Value','Bond type']
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)
    # print(df['Bond type'])
    # df['Bond type'] = df['Bond type'].apply(lambda x: bond_names[df_series['label']])
    df['Bond type'] = bond_names2[link[7]]
    print(df)
    # print(df)
    return df
frames = [get_df(link) for link in links]
master_df = pd.concat(frames)
#columns :
#date, bond type, bond type
# print(master_df)

# print(df.head())

'''Name: 0, dtype: object
>>> df_series['label']
'V39056'
>>> df_series['id']
'BD.CDN.LONG.DQ.YLD'
>>> df_series['description']
'Government of Canada Benchmark Bond Yields - Long-Term'
>>> df_series.size
3
>>>
'''
'''id                                            BD.CDN.LONG.DQ.YLD
label                                                     V39056
description    Government of Canada Benchmark Bond Yields - L...
Name: 0, dtype: object
'''
'''           id label description
3     2001-01-02  5.52         NaN
4     2001-01-03  5.63         NaN
5     2001-01-04  5.62         NaN'''

#returns df that is date(index, datetime format), bond type, value
