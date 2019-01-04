'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''
import tensorflow.keras as keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Flatten
from tensorflow.keras.layers import Conv2D,MaxPooling2D
from tensorflow.keras import backend as K
import time

from clusterweb.pbs import qsub
from clusterweb.pbs import qstat

batch_size = 128
n_classes = 10
epochs = 1

h,w = 28,28

if K.image_data_format() == 'channels_first':
    input_shape = (1,h,w)
else:
    input_shape = (h,w,1)


def get_data():
    (x_train,y_train),(x_test,y_test) = mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0],1,h,w)
        x_test = x_test.reshape(x_test.shape[0],1,h,w)
    else:
        x_train = x_train.reshape(x_train.shape[0],h,w,1)
        x_test = x_test.reshape(x_test.shape[0],h,w,1)

    x_train = x_train.astype('float32')/255
    x_test = x_test.astype('float32')/255

    y_train = keras.utils.to_categorical(y_train,n_classes)
    y_test = keras.utils.to_categorical(y_test,n_classes)

    return x_train,y_train,x_test,y_test


def make_model():
    model = Sequential()
    model.add(Conv2D(32,kernel_size=(3,3),
                   activation='relu',
                   input_shape=input_shape))
    model.add(Conv2D(64,(3,3),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128,activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(n_classes,activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                optimizer='adam',
                metrics=['accuracy'])
    return model


def train(epochs):
    x_train,y_train,x_test,y_test = get_data()

    model = make_model()

    model.fit(x_train,y_train,
        batch_size=batch_size,
        epochs=epochs,
        verbose=1,
        validation_data=(x_test,y_test))

    return model.get_weights()


def main():
    __,___,x_test,y_test = get_data()

    q = qsub.Qsub(train,1)
    q.push()
    q.pull()

    while not q.complete:
        time.sleep(1)

    model = make_model()
    weights = q.result
    print(weights)
    model.set_weights(weights)

    score = model.evaluate(x_test,y_test,verbose=0)
    print('Test loss:',score[0])
    print('Test accuracy:',score[1])

if __name__ == "__main__":
    main()












