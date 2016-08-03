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
    train_data = train_data.drop(['gender', 'age'], axis=1)
    return train_data


def get_histogram(feature):
    events = read_or_load_raw_file('../data/events.csv')
    app_labels = read_or_load_raw_file('../data/app_labels.csv')
    app_events = read_or_load_raw_file('../data/app_events.csv')
    label_categories = read_or_load_raw_file('../data/label_categories.csv')
    # This makes the histogram, will add counts
    histogram = label_categories['label_id']

    return histogram
    
	
def get_processed_train_data():
    raw_train_data = get_raw_train_data()
    phone_brand_model = read_or_load_raw_file('../data/phone_brand_device_model.csv')
    events = read_or_load_raw_file('../data/events.csv')
    app_labels = read_or_load_raw_file('../data/app_labels.csv')
    # Temporary for testing
    processed_train_data = raw_train_data.head(1)
    processed_train_data = pd.merge(processed_train_data, phone_brand_model, on=['device_id'])
#    processed_train_data['installed_apps_histogram'] = get_histogram('installed')
#    processed_train_data['active_apps_histogram'] = get_histogram('active')

    # remove the id at the end
    # processed_train_data = processed_train_data.drop('device_id', axis=1)
    return processed_train_data


def get_processed_test_data():
    raw_test_data = get_raw_test_data()
    return raw_test_data

