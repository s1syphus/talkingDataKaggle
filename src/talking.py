"""
    Kaggle Competition talking data

    Possibly drop data where no events exist

"""

from __future__ import division

import talking_data as td
import pandas as pd
# import training stuff here
# tree, neural network, etc.


td.read_load_all_data()
train = td.get_processed_train_data()
# probably should save this at some point
events = td.read_or_load_raw_file('../data/events.csv')
# make this easier to use
events = events.drop(['timestamp', 'longitude', 'latitude'], axis=1)
app_events = td.read_or_load_raw_file('../data/app_events.csv')
app_labels = td.read_or_load_raw_file('../data/app_labels.csv')
label_categories = td.read_or_load_raw_file('../data/label_categories.csv')
# histogram_installed = td.get_histogram(-8260683887967679142, 'installed')
# test = td.get_processed_test_data()

# Move this to histogram after working

# Easier bookkeeping
all_label_ids = label_categories['label_id'];

device_id = 8663743929678393765
events_for_device = events[events['device_id'] == device_id].drop(['device_id'], axis=1)
app_events = app_events.drop(['is_installed', 'is_active'], axis=1);
apps_for_device = app_events.merge(events_for_device, on='event_id')
apps_for_device = apps_for_device.drop('event_id', axis=1)
# I think I need to do this to get the unique apps
# There is potentially more data in here but I don't know how to use it effectively
apps_for_device = apps_for_device['app_id'].unique()


histogram = all_label_ids.


# create submission stuff


