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


def get_installed_histograms(device_ids):
    # At some point this should be optimized
    histograms = pd.DataFrame(device_ids)
    events = read_or_load_raw_file('../data/events.csv')
    events = events.drop(['timestamp', 'longitude', 'latitude'], axis=1)
    app_events = read_or_load_raw_file('../data/app_events.csv')
    app_labels = read_or_load_raw_file('../data/app_labels.csv')
    label_categories = read_or_load_raw_file('../data/label_categories.csv')
    for device_id in device_ids:
        events_for_device = events[events['device_id'] == device_id].drop(['device_id'], axis=1)
        apps_for_device = app_events.merge(events_for_device, on='event_id')
        apps_for_device = apps_for_device.drop('event_id', axis=1)
        apps_for_device = apps_for_device.drop_duplicates()
        labels_for_device = app_labels.merge(apps_for_device, on='app_id').drop('app_id', axis=1).drop_duplicates(
            'label_id')
        hist = label_categories['label_id'].isin(labels_for_device['label_id']).astype(int).to_frame().drop('label_id', axis=1).transpose()
        hist['device_id'] = device_id
        histograms = histograms.append(hist)
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
        processed_train_data = raw_train_data.head(10)
        processed_train_data = pd.merge(processed_train_data, phone_brand_model, on=['device_id'])
        # Breaking this apart for clarity
        hists = get_installed_histograms(processed_train_data['device_id'])
        processed_train_data = pd.merge(processed_train_data, hists, on=['device_id'])
    #    processed_train_data['active_apps_histogram'] = get_histogram('active')

        # remove the id at the end
        processed_train_data = processed_train_data.drop('device_id', axis=1)
        processed_train_data = processed_train_data.fillna(0)
        processed_train_data.to_pickle(pickled_name)
        return processed_train_data


def get_processed_test_data():
    raw_test_data = get_raw_test_data()
    return raw_test_data

