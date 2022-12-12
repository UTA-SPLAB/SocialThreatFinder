import tensorflow as tf 
import numpy as np
from matplotlib import pyplot as plt
import os


from tensorflow.keras.models import load_model

import cv2
new_model = load_model('drivers/cnn_image_phishing/stf_phish.h5')


def run_model(i): # i = full path of image to predict
    img = cv2.imread(f'{i}')

    resize = tf.image.resize(img, (256,256))

    yhat = new_model.predict(np.expand_dims(resize/255, 0))

    #print(yhat)

    if yhat > 0.7: 
        print(f'Image {i} is Phishing')
        return 'Phishing',str(yhat[0][0])
    
    elif yhat < 0.7 and yhat >0.5:
        return 'Unsure',str(yhat[0][0])

    else:
        print(f'Image {i} is Benign')
        #file.write(f"\n{i},phishing,benign") # filename,Actual, predicted
        return 'Benign',str(yhat[0][0])

# Example run
# run_model("test_images/phish/204.png")
