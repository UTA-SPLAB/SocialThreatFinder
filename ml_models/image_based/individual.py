import tensorflow as tf 
import numpy as np
from matplotlib import pyplot as plt
import time
import os

from tensorflow.keras.models import load_model

new_model = load_model('ml_models/image_based/models/phish_benign.h5')

# Predict a new image

import cv2

def check_if_phish(image_name): # set_folder={inactive,phish}
    
    img_path=f'screens/{image_name}'
    
    img = cv2.imread(img_path)
    
    resize = tf.image.resize(img, (256,256))

    yhat = new_model.predict(np.expand_dims(resize/255, 0))

    print(yhat)

    if yhat > 0.5: 
        #print(f'Image {i} is Phishing')
        return 1
    else:
        #print(f'Image {i} is Benign')
        return 0


