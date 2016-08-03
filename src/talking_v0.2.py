"""
    Driver file
"""

import load_talking_data
import datetime
import tree_approach
import neural_network_approach


def create_submission(score, test, prediction):
    # Make Submission
    now = datetime.datetime.now()
    sub_file = '../submissions/submission_' + str(score) + '_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    print('Writing submission: ', sub_file)
    f = open(sub_file, 'w')
    f.write('device_id,F23-,F24-26,F27-28,F29-32,F33-42,F43+,M22-,M23-26,M27-28,M29-31,M32-38,M39+\n')
    total = 0
    test_val = test['device_id'].values
    for i in range(len(test_val)):
        str1 = str(test_val[i])
        for j in range(12):
            str1 += ',' + str(prediction[i][j])
        str1 += '\n'
        total += 1
        f.write(str1)
    f.close()

train = load_talking_data.read_or_load_train()
test = load_talking_data.read_or_load_test()
# Features
features = list(test.columns.values)
features.remove('device_id')

# test_prediction, score = tree_approach.train_and_test_xgb(train, test, features, 'group')
# neural_network_approach.train_and_test(train, test)

# test_prediction, score = neural_network_approach.train_and_test(train, test, features, 'group')
# print("LS: {}".format(round(score, 5)))
# create_submission(score, test, test_prediction)
