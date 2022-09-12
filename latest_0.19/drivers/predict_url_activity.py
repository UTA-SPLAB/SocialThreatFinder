import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Hide Tensoflow console log
import tensorflow as tf 
import numpy as np
from matplotlib import pyplot as plt
import time



from tensorflow.keras.models import load_model

# full path
#new_model = load_model('drivers/pretrained/inactive_phish.h5')


#short path for testing

new_model = load_model('drivers/pretrained/inactive_phish.h5')

# Predict a new website

import cv2

def check_if_active_ml(image_name): # set_folder={inactive,phish}
    
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

# Test

#check_if_phish('1569110987990798337.png')

