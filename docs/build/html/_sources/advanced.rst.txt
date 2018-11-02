Advanced Usage Tutorials
========================


Portable Batch System Examples:
###############################


Connect to Multiple Clusters
----------------------------

.. note:: Under Construction: Coming Soon


Compare Muliple Clusters' Performance
-------------------------------------

.. note:: Under Construction: Coming Soon

Train a Keras CNN Remotely and Retrieve the Weights
---------------------------------------------------

Neural Networks are costly to compute but also may require much
fine tuning. Here, a model that is developed locally is sent
to the cluster without having to manually transfer any model
files. 


The weights are sent back since sending back a matrix of weights 
is much simpler for the serialization process than the unreliable process 
of serializing entire models. This also allows for a smaller data transfer 
which speeds up the process as it is the most costly component.

The Keras library is installed both separate from the main
TensorFlow library as well as being included in the TensorFlow
package. For your cluster, you may need to change the import 
commands to include your version of Keras. 

.. code-block:: python

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
	    model.set_weights(weights)

	    score = model.evaluate(x_test,y_test,verbose=0)
	    print('Test loss:',score[0])
	    print('Test accuracy:',score[1])

	if __name__ == "__main__":
	    main()

Run Inference on an Image from a Webcam Remotely
------------------------------------------------

The importance of remote compute to IoT applications needs no introduction. 
In this example, OpneCV is used to take a picture while a pretrained network 
runs inference on it on a remote nod. This is a simple example that is not 
efficient as each instance must load the model. 

.. code-block:: python

	from keras.applications import vgg16
	from keras.preprocessing import image
	from keras.applications.resnet50 import preprocess_input,decode_predictions
	import numpy as np
	import time
	import cv2

	from clusterweb.pbs import qsub
	from clusterweb.pbs import qstat

	def take_picture():
	    video_data = cv2.VideoCapture(0)
	    print("Press any key to take a picture")

	    while True:
	        _,frame = video_data.read()
	        h,w = frame.shape[:2]

	        frame = frame[int(h/2)-224:int(h/2)+224,
	            int(w/2)-224:int(w/2)+224]

	        frame = cv2.resize(frame,(224,224))

	        cv2.imshow('frame',frame)
	        k = cv2.waitKey(1)
	        if k != -1:
	            break

	    cv2.destroyAllWindows()
	    cv2.waitKey(1)
	    return preprocess_input(np.expand_dims(frame,axis=0))

	def job(frame):
	    model = vgg16.VGG16(weights='imagenet')
	    return model.predict(frame)

	def main():
	    x = take_picture()
	    q = qsub.Qsub(job,x)
	    q.push()
	    q.pull()

	    while not q.complete:
	        time.sleep(1)

	    preds = q.result
	    print('Predicted:',decode_predictions(preds, top=10)[0]) 
	    
	if __name__ == "__main__":
	    main()

Secure Shell System Examples:
#############################


Using Basic Locks
-----------------

.. note:: Under Construction: Coming Soon

Using Semaphores
----------------

.. note:: Under Construction: Coming Soon

Setup a TCP Server on Remote Device
-----------------------------------

.. note:: Under Construction: Coming Soon

Setup an OSC Server on a Remote Device
--------------------------------------

.. note:: Under Construction: Coming Soon

Create a Chat Session with Multiple User Devices
------------------------------------------------

.. note:: Under Construction: Coming Soon


