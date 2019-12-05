from data_prep import *
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import lstm, time # Helper functions

def build_model():
    model = Sequential()
    model.add(LSTM(
        input_dim=8,
        output_dim=50,
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        100,
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=1))
    model.add(Activation('linear'))
    start = time.time()
    model.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])
    print('completion time: {}'.format(time.time()-start))
    return model

def train_model(model, X_train, y_train, batch_size, nb_epoch, validation_split):
    model.fit(
        X_train,
        y_train,
        batch_size,
        nb_epoch,
        validation_split)

if __name__ == '__main__':
    path = r'C:\Users\945970\Desktop\random_learning_projects\FX\data'
    full_data = merge_all_csvs(path)
    full_data, fx_USJPY = feature_engineering(full_data)
    ## Load the data using the helper function
    X = full_data.drop('close', axis=1).values
    y = full_data[['close']].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    model = build_model()
    train_model(model, X_train, y_train, batch_size=512, nb_epoch=1, validation_split=0.05)
    predictions = lstm.predict_point_by_point(model, X_test)
    lstm.plot_results_multiple(predictions, y_test, 1)
