from keras.applications import vgg16, inception_v3, resnet50, mobilenet
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
    print('Predicted:',decode_predictions(preds,top=10)[0]) 
    
if __name__ == "__main__":
    main()