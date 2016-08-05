"""
    Kaggle Competition talking data read/load/pre-process
"""

import pandas as pd
import os
import glob
from sklearn.preprocessing import LabelEncoder
import time


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


def get_installed_histograms(device_ids):
    histograms = pd.DataFrame(device_ids)
    device_ids = pd.DataFrame(device_ids)
    events = read_or_load_raw_file('../data/events.csv')
    events = events.drop(['timestamp', 'longitude', 'latitude'], axis=1)
    app_events = read_or_load_raw_file('../data/app_events.csv')
    app_labels = read_or_load_raw_file('../data/app_labels.csv')
    label_categories = read_or_load_raw_file('../data/label_categories.csv')
    events_for_device = device_ids.merge(events, on='device_id')
    del events
    apps_for_device = events_for_device.merge(app_events, on='event_id')
    del events_for_device
    labels_for_device = apps_for_device.merge(app_labels, on='app_id')

    all_hists = pd.DataFrame()

    start_time = time.time()

    print(device_ids.count())

    for index, row in device_ids.iterrows():
        if index % 1000 == 0:
            print(index)
            print('Loading time: {} minutes'.format(round((time.time() - start_time) / 60, 2)))
        labels_for_one_device = labels_for_device[labels_for_device['device_id'] == row['device_id']]['label_id']
        hist = label_categories['label_id'].isin(labels_for_one_device).astype(int).to_frame().transpose()
        hist['device_id'] = row['device_id']
        all_hists = all_hists.append(hist)

    histograms = histograms.merge(all_hists, on='device_id', how='left')

    return histograms


def get_processed_train_data():
    # Check if exists
    pickled_name = '../data/pickled/processed_train_data.pkl'
    if os.path.isfile(pickled_name):
        return pd.read_pickle(pickled_name)
    else:
        raw_train_data = get_raw_train_data()
        phone_brand_model = read_or_load_raw_file('../data/phone_brand_device_model.csv')
        # Temporary for testing
        processed_train_data = raw_train_data
        processed_train_data = pd.merge(processed_train_data, phone_brand_model, on=['device_id'])
        # Breaking this apart for clarity
        hists = get_installed_histograms(processed_train_data['device_id'])
        processed_train_data = pd.merge(processed_train_data, hists, on=['device_id'])
        # Maybe do this at some point
        # processed_train_data['active_apps_histogram'] = get_histogram('active')

        # remove the id at the end
        processed_train_data = processed_train_data.drop('device_id', axis=1)
        processed_train_data = processed_train_data.fillna(-1)
        processed_train_data = processed_train_data.apply(LabelEncoder().fit_transform)
        processed_train_data.to_pickle(pickled_name)
        return processed_train_data


def get_processed_test_data():
    # Check if exists
    pickled_name = '../data/pickled/processed_test_data.pkl'
    if os.path.isfile(pickled_name):
        return pd.read_pickle(pickled_name)
    else:
        raw_test_data = get_raw_test_data()
        phone_brand_model = read_or_load_raw_file('../data/phone_brand_device_model.csv')
        # Temporary for testing
        processed_test_data = raw_test_data
        processed_test_data = pd.merge(processed_test_data, phone_brand_model, on=['device_id'])
        # Breaking this apart for clarity
        hists = get_installed_histograms(processed_test_data['device_id'])
        processed_test_data = pd.merge(processed_test_data, hists, on=['device_id'])
        # Maybe do this at some point
        # processed_train_data['active_apps_histogram'] = get_histogram('active')

        # remove the id at the end
        processed_test_data = processed_test_data.drop('device_id', axis=1)
        processed_test_data = processed_test_data.fillna(-1)
        processed_test_data = processed_test_data.apply(LabelEncoder().fit_transform)
        processed_test_data.to_pickle(pickled_name)
        return processed_test_data

