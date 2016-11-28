# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:21:55 2016

@author: Greta
"""
import cv2
import mouth_recognition
# import prepare_dataset
from sklearn.externals import joblib

# load the model
model = joblib.load('svc_1.pkl')


# ----------------------- PREDICTION ----------------------
def prediction(im):
    scale = 1.1
    neighbors = 25
    # from matplotlib.patches import Rectangle
    # ax = gca()
    # ax.imshow(im, cmap='gray')
    # detected_faces=mouth_recognition.find_face(im)
    # for (x, y, w, h) in detected_faces:
        # ax.add_artist(Rectangle((x, y), w, h, fill=False, lw=5, color='blue'))

    detected_mouth = mouth_recognition.find_mouth(im, scale, neighbors, 1)
    size = [40, 80]
    if detected_mouth != []:
        value_predict = model.predict(detected_mouth.reshape(1, size[0] * size[1]))
        # print(value_predict)
        return value_predict[0]
    else:
        print('Mouth not found')
        return 0


# ----------------- EMOTION RECOGNITION ---------------------------
def emotion_recognition(image):
    return prediction(image)


# img = cv2.imread("smile.jpg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# emotion_recognition(gray)
## Draw a rectangle around the faces
#img = cv2.imread("webcam_normal.jpg")
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#emotion_recognition(gray)
#
#img = cv2.imread("webcam_happy.jpg")
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#emotion_recognition(gray)
