# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:21:55 2016

@author: Greta
"""
import prediction
# import cv2
#import prepare_dataset
from sklearn.externals import joblib

def emotion_recognition(image):

    model=joblib.load('svc_1.pkl')
    return prediction.prediction(image,model)


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