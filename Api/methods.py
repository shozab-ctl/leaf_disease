from keras import utils
import logging
import json
import pickle
from logging.config import dictConfig
import numpy as np
import cv2
from flask import abort
from PIL import Image
from keras.models import load_model
import tensorflow as tf
from tensorflow.keras.preprocessing import image as img
from tensorflow.keras.utils import load_img, img_to_array
def run_model(img):
    try :
       model = tf.keras.models.load_model('model2.h5')
       
    except FileNotFoundError as e :        
       return abort('Unable to find the file: %s.' % str(e), 503)
    pred = model.predict(img)
    prediction = pred
    return prediction
def load_image(filename):
    image = img.load_img(filename,target_size=(256,256))
    x = img_to_array(image)
    x = np.expand_dims(x, axis=0)
    return x
def classify(data):
    upload = data
    image = load_image(upload)
    #load_image() is to process image :
    print('image ready')
    try:
        prediction = run_model(image)
        label=pickle.load(open('label_transform.pkl','rb'))

        return (json.dumps({"prediction": str(label.inverse_transform(prediction)[0])}))
    except FileNotFoundError as e:
        return abort('Unable to locate image: %s.' % str(e), 503)
    except Exception as e:
        return abort('Unable to process image: %s.' % str(e), 500)






