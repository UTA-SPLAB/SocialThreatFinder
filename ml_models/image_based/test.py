import tensorflow as tf 
import numpy as np
from matplotlib import pyplot as plt
import time
import os

from tensorflow.keras.models import load_model

new_model = load_model('models/phish_benign.h5')

# Predict a new image

import cv2

phish_images = os.listdir(f'tests/phish/')
inactive_images=os.listdir(f'tests/inactive')


def run_model(set_folder,image_name): # set_folder={inactive,phish}
    
    img_path=f'tests/{set_folder}/{image_name}'
    
    img = cv2.imread(img_path)
    
    plt.imshow(img)

    resize = tf.image.resize(img, (256,256))

    yhat = new_model.predict(np.expand_dims(resize/255, 0))

    print(yhat)

    if yhat > 0.5: 
        #print(f'Image {i} is Phishing')
        return 1
    else:
        #print(f'Image {i} is Benign')
        return 0


# Check phishing samples


def evaluate(set_folder):

    print(f'============= Testing on {set_folder} set ===============')
    i=0
    phish_count=0
    while i<500:
        if set_folder=='phish':
            image_name=phish_images[i]
        elif set_folder=='inactive':
            image_name=inactive_images[i]

        verdict=run_model(set_folder,image_name)
        if verdict==1:
            phish_count=phish_count+1

        i=i+1
        
    phish_accuracy=(phish_count/500)*100
    print(f'No of images marked as phish: {phish_count}')


evaluate('inactive')
evaluate('phish')