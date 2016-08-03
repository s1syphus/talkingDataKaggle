"""
    Neural network approach
"""
from keras.models import Sequential
from keras.layers import Dense, Activation


def train_and_test(train, test):
    print(train)
    print(test)
    '''
    model = Sequential()
    model.add(Dense(output_dim=10, input_dim=))
    model.add(Activation("relu"))
    model.add(Dense(output_dim=10))
    model.add(Activation("softmax"))
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)
    proba = model.predict_proba(X_test, batch_size=32)
    '''
