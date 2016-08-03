"""
    Using keras

    Right now the data is just raw. Later will, preprocess
"""
import os
import pandas as pd
import numpy as np
import glob


def read_or_load_file(file_path):
    pickled_name = '../data/pickled/' + os.path.basename(file_path) + '.pkl'
    if os.path.isfile(pickled_name):
        print('Loading ', file_path, '...')
        loaded_file = pd.read_pickle(pickled_name)
    else:
        print('Reading...')
        loaded_file = pd.read_csv(file_path, dtype={'device_id': np.str})
        loaded_file.to_pickle(pickled_name)
    return loaded_file


def read_load_all_data():
    all_file_names = glob.glob('../data/*.csv')
    for file_name in all_file_names:
        read_or_load_file(file_name)
    return


read_load_all_data()


