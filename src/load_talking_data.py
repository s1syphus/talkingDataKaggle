"""
    This loads the talking data
"""

import numpy as np
import pandas as pd
import os


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


def read_or_load_train():
    pickled_name = '../data/pickled/train.pkl'
    if os.path.isfile(pickled_name):
        return pd.read_pickle(pickled_name)
    else:
        train_file = '../data/gender_age_train.csv'
        train = read_or_load_file(train_file)
        train = map_column(train, 'group')
        train = train.drop(['age'], axis=1)
        train = train.drop(['gender'], axis=1)
        train = pd.merge(train, read_or_load_phone_brand(), how='left', on='device_id', left_index=True)
        train = pd.merge(train, read_or_load_events(), how='left', on='device_id', left_index=True)
        train.fillna(-1, inplace=True)
        train.to_pickle(pickled_name)
        return train


def read_or_load_test():
    pickled_name = '../data/pickled/test.pkl'
    if os.path.isfile(pickled_name):
        return pd.read_pickle(pickled_name)
    else:
        test_file = '../data/gender_age_test.csv'
        test = read_or_load_file(test_file)
        test = pd.merge(test, read_or_load_phone_brand(), how='left', on='device_id', left_index=True)
        test = pd.merge(test, read_or_load_events(), how='left', on='device_id', left_index=True)
        test.fillna(-1, inplace=True)
        test.to_pickle(pickled_name)
        return test


def read_or_load_events():
    event_file = '../data/events.csv'
    events = read_or_load_file(event_file)
    events['counts'] = events.groupby(['device_id'])['event_id'].transform('count')
    events_small = events[['device_id', 'counts']].drop_duplicates('device_id', keep='first')
    return events_small


def read_or_load_phone_brand():
    phone_brand_file = '../data/phone_brand_device_model.csv'
    phone_brand = read_or_load_file(phone_brand_file)
    phone_brand.drop_duplicates('device_id', keep='first', inplace=True)
    phone_brand = map_column(phone_brand, 'phone_brand')
    phone_brand = map_column(phone_brand, 'device_model')
    return phone_brand


def map_column(table, f):
    labels = sorted(table[f].unique())
    mappings = dict()
    for i in range(len(labels)):
        mappings[labels[i]] = i
    table = table.replace({f: mappings})
    return table


train = read_or_load_train()
test = read_or_load_test()
# Features
features = list(test.columns.values)
features.remove('device_id')
print('Length of train: ', len(train))
print('Length of test: ', len(test))
print('Features [{}]: {}'.format(len(features), sorted(features)))
