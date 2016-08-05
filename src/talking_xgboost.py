"""
    XGBoost stuff for talking data
"""

import xgboost as xgb
from sklearn.cross_validation import train_test_split
from sklearn.metrics import log_loss
import time
import random

random.seed(2016)


def run_xgb(train, test, features, target, random_state=0):
    return


