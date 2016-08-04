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
# histogram_installed = td.get_installed_histogram_for_device(-8260683887967679142)
# hists = td.get_installed_histograms(train['device_id'])
# test = td.get_processed_test_data()

# device_id = 29182687948017175
#
# test_device = train[train['device_id'] == 29182687948017175]['device_id']



# hist = pd.DataFrame()
#
# for x in label_categories:
#     hist[x['label_id']] = x['label_id'].isin([labels_for_device])



# create submission stuff


