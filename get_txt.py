'''
gets the text files from
https://sundowner.colorado.edu/weather/atoc1/archive_index.html
'''

import numpy as np
import urllib.request
from datetime import datetime, timedelta

BASE_URL = 'https://sundowner.colorado.edu/weather/atoc1'

DAYS_IN_MONTH = {
    'Jan': 31,
    'Feb': 28,
    'Mar': 31,
    'Apr': 30,
    'May': 31,
    'Jun': 30,
    'Jul': 31,
    'Aug': 31,
    'Sep': 30,
    'Oct': 31,
    'Nov': 30,
    'Dec': 31
}

# rows of the data
ROWS = ['Date', 'Time', 'Temp Out', 'Hi Temp', 'Low Temp', 'Out Hum',
        'Dew Pt.', 'Wind Speed', 'Wind Dir', 'Wind Run', 'Hi Speed',
        'Hi Dir', 'Wind Chill', 'Heat Index', 'THW Index', 'THSW Index',
        'Bar', 'Rain', 'Rain Rate', 'Solar Rad.', 'Solar Energy',
        'Hi Solar Rad.', 'Heat D-D', 'Cool D-D', 'In Temp',
        'In Hum', 'In Dew', 'In Heat', 'In EMC', 'In Air Density',
        'ET', 'Wind Samp', 'Wind Tx', 'ISS Recept', 'Arc. Int.']


def get_txt_file(year, month, day):
    '''
    gets the text file with the desired year, month, and day
    '''
    # the actual text filename on the website is 1 day ahead
    date_for_url = datetime(year=year, month=month, day=day) + timedelta(days=1)

    correct_year = date_for_url.year

    correct_month = date_for_url.month
    correct_day = date_for_url.day

    year_str = str(correct_year)
    month_str = str(correct_month)
    day_str = str(correct_day)

    if len(month_str) == 1:
        month_str = f'0{month_str}'

    if len(day_str) == 1:
        day_str = f'0{day_str}'

    url = f'{BASE_URL}/wxobs{year_str}{month_str}{day_str}.txt'

    data = urllib.request.urlopen(url)
    data_arr = []
    for line in data:
        data_arr.append(line)

    for idx, row in enumerate(data_arr[3:]):
        split_row = row.split()
        rows = [item.decode('UTF-8') for item in split_row]
        print(len(rows))
        print((rows))


if __name__ == '__main__':
    get_txt_file(2020, 1, 1)