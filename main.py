import numpy as np

from epw import epw


import pathlib
import shutil
import pandas as pd

from datetime import datetime, timedelta
from numpy.core.numeric import full

from numpy.lib.shape_base import split

import get_txt

def datetime_range(start=None, end=None):
    span = end - start
    for i in range(span.days + 1):
        yield start + timedelta(days=i)

def load_epw_file():
    pass

def direction_to_degrees(x):
    if x in DIR_TO_DEG_DICT:

        return DIR_TO_DEG_DICT[x]
    else:
        return 0


def fahrenheit_2_celsius(degrees):
    try:
        degrees = float(degrees)
        return (degrees - 32) * (5 / 9)
    except:
        return np.nan

def identity_function(x):
    """
    does nothing to the input
    """
    return x

def mph_2_ms(x):
    """
    converts mph to m/s
    """
    try:
        x = float(x)
        return x * 0.44704
    except:
        return np.nan

# second item in dict entry/item is a function
TXT_TO_EPW_DICT = {
    'Temp Out': ['Dry Bulb Temperature', fahrenheit_2_celsius],
    'Out Hum': ['Relative Humidity', identity_function],
    'Dew Pt.': ['Dew Point Temperature', fahrenheit_2_celsius],
    'Wind Speed': ['Wind Speed', mph_2_ms],
    'Wind Dir': ['Wind Direction', direction_to_degrees],
    'Solar Rad.': ['Direct Normal Radiation', identity_function]
}

DIR_TO_DEG_DICT = {
    'N': 0,
    'NNE': 22.5,
    'NE': 45,
    'ENE': 67.5,
    'E': 90,
    'ESE': 112.5,
    'SE': 135,
    'SSE': 157.5,
    'S': 180,
    'SSW': 202.5,
    'SW': 225,
    'WSW': 247.5,
    'W': 270,
    'WNW': 292.5,
    'NW': 315,
    'NNW': 337.5
}



if __name__ == '__main__':
    directory = (pathlib.Path(__file__).parent.absolute())
    # shutil.copyfile(f'{directory}/', f'{directory}/')
    original_fname = 'USA_CO_Boulder-Broomfield-Jefferson.County.AP.724699_TMY3.epw'
    whole_filename = f'{directory}/{original_fname}'

    epw_obj = epw()
    epw_obj.read(whole_filename)
    headers = epw_obj.headers
    epw_df = epw_obj.dataframe

    # epw df
    # test_series = pd.Series(np.ones(20000))
    # epw_df.loc[:, 'Wind Speed'] = test_series
    # print(epw_df['Wind Speed'])

    # replace the year here
    year = 2018

    x = list(datetime_range(start=datetime(year, 1, 1), end=datetime(year, 12, 31)))

    txt_df = get_txt.get_txt_file_df(year, 1, 1)
    print(year, 1, 1)
    for item in x[1:]:
        txt_df1 = get_txt.get_txt_file_df(item.year, item.month, item.day)
        txt_df = pd.concat([txt_df, txt_df1], ignore_index=True)
        print(item.year, item.month, item.day)

    len_txt_df = len(txt_df)
    new_rows = [pd.Series() for _ in range(1000)]

    for i in range((len_txt_df // 1000) + 1):
        print(len(epw_df))
        epw_df = epw_df.append(new_rows, ignore_index=True)

    for key in TXT_TO_EPW_DICT:

        try:
            res = txt_df[key].apply(lambda x: TXT_TO_EPW_DICT[key][1](x))
            print((epw_df[TXT_TO_EPW_DICT[key][0]]))
            epw_df.loc[:, TXT_TO_EPW_DICT[key][0]] = res
            print((epw_df[TXT_TO_EPW_DICT[key][0]]))
        except Exception as e:
            print(e)
            print("Failure!")

    # text df
    # deal with date separately
    num_dates = len(txt_df['Date'].values)

    year_list = []
    month_list = []
    day_list = []
    
    hour_list = []
    minute_list = []

    for idx in range(len(txt_df['Date'].values)):
        date = txt_df['Date'].values[idx]
        time = txt_df['Time'].values[idx]
        splits = time.split(':')
        tod = splits[1][-1]
        if tod == 'p' and splits[0] != '12':
            splits[0] = str(int(splits[0]) + 12)

        if tod == 'a' and splits[0] == '12':
            splits[0] = str(00)

        splits[1] = splits[1][:-1]
        
        if len(splits[0]) == 1:
            splits[0] = f'0{splits[0]}'
        full_time = f'{splits[0]}:{splits[1]}'

        # parse the date
        split_date = date.split('/')
        should_add_zero = False
        if len(split_date[0]) == 1:
            should_add_zero = True
        if should_add_zero:
            date = f'0{date}'

        year_list.append(f'20{split_date[2]}')
        month_list.append(f'{split_date[0]}')
        day_list.append(f'{split_date[1]}')

        hour_list.append(f'{splits[0]}')
        minute_list.append(f'{splits[1]}')

        epw_df['Year'].values[idx] = f'20{split_date[2]}'
        epw_df['Month'].values[idx] = f'{split_date[0]}'
        epw_df['Day'].values[idx] = f'{split_date[1]}'
        epw_df['Hour'].values[idx] = f'{splits[0]}'
        epw_df['Minute'].values[idx] = f'{splits[1]}'
        
    df_filtered = epw_df[epw_df['Year'] == year]
    df_filtered.loc[:, 'Year'] = df_filtered['Year'].astype(int)
    df_filtered.loc[:, 'Month'] = df_filtered['Month'].astype(int)
    df_filtered.loc[:, 'Day'] = df_filtered['Day'].astype(int)
    df_filtered.loc[:, 'Hour'] = df_filtered['Hour'].astype(int)
    df_filtered.loc[:, 'Minute'] = df_filtered['Minute'].astype(int) 
    print(len(df_filtered))
    print(df_filtered['Year'])
    epw_obj.dataframe = df_filtered

    epw_obj.write(f'{year}_modified.epw')