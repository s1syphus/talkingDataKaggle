"""
    Kaggle Competition talking data
"""

from __future__ import division

import talking_data as td
import pandas as pd
# import training stuff here
# tree, neural network, etc.


td.read_load_all_data()
train = td.get_processed_train_data()
events = td.read_or_load_raw_file('../data/events.csv')
app_events = td.read_or_load_raw_file('../data/app_events.csv')
app_labels = td.read_or_load_raw_file('../data/app_labels.csv')
label_categories = td.read_or_load_raw_file('../data/label_categories.csv')
histogram_installed = td.get_histogram('installed')
# test = td.get_processed_test_data()

# create submission stuff

