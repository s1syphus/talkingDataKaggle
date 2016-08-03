"""
    Kaggle Competition talking data read/load/pre-process
"""

import pandas as pd
import os
import glob


def read_or_load_raw_file(file_path):
    """
        This reads/loads from pickle a raw file
        No processing occurs here
    :param file_path:
    :return:
    """
    pickled_name = '../data/pickled/' + os.path.basename(file_path) + '.pkl'
    if os.path.isfile(pickled_name):
        loaded_file = pd.read_pickle(pickled_name)
    else:
        loaded_file = pd.read_csv(file_path)
        loaded_file.to_pickle(pickled_name)
    return loaded_file


def read_load_all_data():
    """
        This function makes sure all csv files are pickled for faster access
    :return:
    """
    all_file_names = glob.glob('../data/*.csv')
    for file_name in all_file_names:
        read_or_load_raw_file(file_name)
    return


def get_raw_test_data():
    """
        Totally raw pandas object being returned, no pre-processing
    """
    return read_or_load_raw_file('../data/gender_age_test.csv')


def get_raw_train_data():
    """
        Mostly raw pandas object being returned, no pre-processing
    """
    train_data = read_or_load_raw_file('../data/gender_age_train.csv')
    # This does not really help us, the group is what is important
    train_data = train_data.drop(['gender', 'age'])
    return train_data



