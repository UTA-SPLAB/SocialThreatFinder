import os
import re
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import requests # To capture image screenshots



def format_url(tweet_text):
      regex_hxxp = '//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
      urls = []
      processed_url = 'Null'
      y = 'Null'

        # if("hxxp" or "hxxps" in full_text):

        # it will return list of all urls found by REGEX.
      urls.append(re.findall(regex_hxxp, tweet_text))


      print(urls)


def crop_whitespace(image): # Crop whitespace in image

  import numpy as np
  import cv2

  img = cv2.imread(image) # Read in the image and convert to grayscale
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
  coords = cv2.findNonZero(gray) # Find all non-zero points (text)
  x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
  rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
  #cv2.imshow("Cropped", rect) # Show it
  #cv2.waitKey(0)
  #cv2.destroyAllWindows()
  cv2.imwrite("rect.jpg", rect) # Save the image



# ============ MAIN DRIVER FOR TEXT EXTRACTION MODULE ==============

def identify_text_from_image(image_url):

  try:

    # Sub-module to download image screenshot

    img_data = requests.get(image_url).content
    with open('image.jpg', 'wb') as handler:
      handler.write(img_data)

    crop_whitespace("image.jpg") # In JPG format 
    im = Image.open("rect.jpg") # the second one 
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('temp_process.jpg')
    text = pytesseract.image_to_string(Image.open('temp_process.jpg'))
    print(text)
    url=format_url(text)
    os.system("rm temp_process.jpg") # Remove temp generated pic
    #os.system("rm image.jpg")
    return url
  except Exception as e:
    print(e)

  # DEBUG RUN



  # image_name="temp2.jpg"

identify_text_from_image("https://i.redd.it/ha9cxhnav2m91.jpg")
