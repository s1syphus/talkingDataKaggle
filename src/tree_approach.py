"""
    This contains the tree stuff
"""


import xgboost as xgb
import time
import random
from sklearn.metrics import log_loss
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import *

random.seed(2000)


def train_and_test_xgb(train, test, features, target, random_state=0):
    # Basic XGB
    eta = 0.2
    # sweep this
    max_depth = 10
    subsample = 0.7
    # sweep this
    colsample_bytree = 0.7
    start_time = time.time()

    print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'
          .format(eta, max_depth, subsample, colsample_bytree))
    params = {
        "objective": "multi:softprob",
        "num_class": 12,
        "booster" : "gbtree",
        "eval_metric": "mlogloss",
        "eta": eta,
        "max_depth": max_depth,
        "subsample": subsample,
        "colsample_bytree": colsample_bytree,
        "silent": 1,
        "seed": random_state,
    }

    # sweep this
    num_boost_round = 1000
    early_stopping_rounds = 75
    test_size = 0.3

    x_train, x_valid = train_test_split(train, test_size=test_size, random_state=random_state)
    print('Length train:', len(x_train.index))
    print('Length valid:', len(x_valid.index))
    y_train = x_train[target]
    y_valid = x_valid[target]
    d_train = xgb.DMatrix(x_train[features], y_train)
    d_valid = xgb.DMatrix(x_valid[features], y_valid)

    watchlist = [(d_train, 'train'), (d_valid, 'eval')]
    gbm = xgb.train(params, d_train, num_boost_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds,
                    verbose_eval=True)
    print("Validating...")
    check = gbm.predict(xgb.DMatrix(x_valid[features]), ntree_limit=gbm.best_iteration)
    score = log_loss(y_valid.tolist(), check)

    print("Predict test set...")
    test_prediction = gbm.predict(xgb.DMatrix(test[features]), ntree_limit=gbm.best_iteration)

    print('Training time: {} minutes'.format(round((time.time() - start_time) / 60, 2)))
    return test_prediction.tolist(), score


