import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D

def get_training_set():
    ## Use the pre-existing dataset from MNIST to train from
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
    print(type(X_train), X_train[0])
    ## Reshape the array to 4 dimentions
    X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
    X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
    input_shape = (28, 28, 1)
    ## The data comes in the form of uint8 with value in the [0, 255].
    ## We will transform it to float32 array with values between 0 and 1
    ## This normalization process is important in any machine learning project
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255
    #print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    return X_train, y_train, X_test, y_test, input_shape

def run_model(X_train, y_train, X_test, y_test, input_shape):
    ## Create CNN
    model = Sequential()
    model.add(Conv2D(filters=28, kernel_size=(1, 1), activation='relu',
                     input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))
    model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu',
                     input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))
    model.add(Dropout(0.25))
    model.add(Conv2D(filters=64, kernel_size=(1, 1), activation='relu',
                     input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))
    ## Flatten 2D arrays for fully connected layers
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x=X_train, y=y_train, epochs=10)
    eval_loss, eval_acc = model.evaluate(X_test, y_test)
    print('Evaluatation Loss: {} - Evaluation Accuracy: {}'.format(eval_loss, eval_acc))

    return model

def save_model(model):
    model.save(filepath + '\\cnn_mnist_model.h5')

if __name__ == '__main__':
    filepath = os.path.dirname(__file__)
    print(filepath)
    X_train, y_train, X_test, y_test, input_shape = get_training_set()
    model = run_model(X_train, y_train, X_test, y_test, input_shape)
    save_model(model)
