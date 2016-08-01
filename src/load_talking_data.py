"""
    This loads the talking data
    This should be basic and should not change much
"""

import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction import DictVectorizer
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
    phone_brand = encode_one_hot(phone_brand, cols=['phone_brand'])
    phone_brand = encode_one_hot(phone_brand, cols=['device_model'])
    return phone_brand


def map_column(table, f):
    labels = sorted(table[f].unique())
    mappings = dict()
    for i in range(len(labels)):
        mappings[labels[i]] = i
    table = table.replace({f: mappings})
    return table


def encode_one_hot(df, cols):
    vec = DictVectorizer()
    vec_data = pd.DataFrame(vec.fit_transform(df[cols].to_dict(outtype='records')).toarray())
    vec_data.columns = vec.get_feature_names()
    vec_data.index = df.index
    df = df.drop(cols, axis=1)
    df = df.join(vec_data)
    return df


def read_load_all_data():
    all_file_names = glob.glob('../data/*.csv')
    all_files = pd.DataFrame()
    for file_name in all_file_names:
        pickled_name = '../data/pickled/' + os.path.basename(file_name) + '.pkl'
        if os.path.isfile(pickled_name):
            my_file = pd.read_pickle(pickled_name)
        else:
            my_file = pd.read_csv(file_name)
            my_file.to_pickle(pickled_name)
        all_files.append(my_file)
    return


read_load_all_data()
