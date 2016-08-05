"""
    Kaggle Competition talking data

    Possibly drop data where no events exist

"""

from __future__ import division

import talking_data as td
import talking_xgboost as tree
import xgboost as xgb
from sklearn.cross_validation import train_test_split
from sklearn.metrics import log_loss
import time
from sklearn.preprocessing import LabelEncoder
import random

random.seed(2016)

# import training stuff here
# tree, neural network, etc.


td.read_load_all_data()
train = td.get_processed_train_data()
# This needs to do stuff properly
test = td.get_processed_test_data()

#
# # This seems to be doing something
#
# #
# le = LabelEncoder()
# le.fit(train.columns.values)
# train.columns = le.transform(train.columns.values)
# test.columns = le.transform(test.columns.values)
#
#
# #
# # # Move this out at some point
# features = list(train.columns.values)
#
# random_state=0
# eta = 0.1
# max_depth = 3
# subsample = 0.7
# colsample_bytree = 0.7
# start_time = time.time()
#
# target = le.transform('group')
#
# print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta, max_depth, subsample, colsample_bytree))
# params = {
#     "objective": "multi:softprob",
#     "num_class": 12,
#     "booster" : "gbtree",
#     "eval_metric": "mlogloss",
#     "eta": eta,
#     "max_depth": max_depth,
#     "subsample": subsample,
#     "colsample_bytree": colsample_bytree,
#     "silent": 1,
#     "seed": random_state,
# }
# num_boost_round = 500
# early_stopping_rounds = 50
# test_size = 0.3
#
# x_train, x_valid = train_test_split(train, test_size=test_size, random_state=random_state)
# print('Length train:', len(x_train.index))
# print('Length valid:', len(x_valid.index))
# y_train = x_train[target]
# y_valid = x_valid[target]
# dtrain = xgb.DMatrix(x_train[features], y_train)
# dvalid = xgb.DMatrix(x_valid[features], y_valid)
#
# watchlist = [(dtrain, 'train'), (dvalid, 'eval')]
# gbm = xgb.train(params, dtrain, num_boost_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds, verbose_eval=True)
# #
# # print("Validating...")
# # check = gbm.predict(xgb.DMatrix(x_valid[features]), ntree_limit=gbm.best_iteration)
# # score = log_loss(y_valid.tolist(), check)
#
# # print("Predict test set...")
# # test_prediction = gbm.predict(xgb.DMatrix(test[features]), ntree_limit=gbm.best_iteration)
#
# print('Training time: {} minutes'.format(round((time.time() - start_time)/60, 2)))
# # return test_prediction.tolist(), score
# #
# #
#
#
#
#
#
# # create submission stuff


