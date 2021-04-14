import numpy as np

from epw import epw

import os

import pathlib
import shutil

import get_txt

def load_epw_file():
    pass


if __name__ == '__main__':
    directory = (pathlib.Path(__file__).parent.absolute())
    # shutil.copyfile(f'{directory}/', f'{directory}/')
    original_fname = 'USA_CO_Boulder-Broomfield-Jefferson.County.AP.724699_TMY3.epw'
    whole_filename = f'{directory}/{original_fname}'

    txt_df = get_txt.get_txt_file_df(2019, 1, 1)
    epw_obj = epw()
    epw_obj.read(whole_filename)
    headers = epw_obj.headers
    print(headers)
    df = epw_obj.dataframe
    print(df)
