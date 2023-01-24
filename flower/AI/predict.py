from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import pickle
import cv2
from io import BytesIO
from PIL import Image
import base64
import os

def detect(base64_string):
    
    image = Image.open(BytesIO(base64.b64decode(base64_string)))
    image = np.asarray(image)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

    args = {'model': 'flower/AI/p6flower.model', 'labelbin': 'flower/AI/lb6.pickle'}
    
    image = cv2.resize(image, (224,224))
    image = image.astype("float") / 255.0
    
    image = img_to_array(image)
    image = np.expand_dims(image, axis = 0)
    
    model = load_model(args["model"])
    lb = pickle.loads(open(args["labelbin"], "rb").read())
    proba = model.predict(image)[0]
    idx = np.argsort(-proba)[:3]
    label = lb.classes_[idx]

    proba = proba[idx].astype(np.float64)
    proba = np.floor(proba*1000)/10
    
    image_name_list = [{'flower1':label[0],'accuracy1':proba[0]},{'flower2':label[1],'accuracy2':proba[1]},{'flower3':label[2],'accuracy3':proba[2]}]

    return image_name_list