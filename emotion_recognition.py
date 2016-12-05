# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:21:55 2016

@author: Greta
"""
import cv2
#import prepare_dataset
from sklearn.externals import joblib

def emotion_recognition(image):
  
    #model=joblib.load('svc_1.pkl')
    fishface=cv2.createFisherFaceRecognizer()
    try:
        fishface.load("trained_emoclassifier.xml")
    except:
        print("no xlm file for fisher model")
    pred,conf=fishface.predict(image)
    print("your emotion is",pred)
    #return prediction.prediction(image,model)
    return pred
        
    
#==============================================================================
# img = cv2.imread("webcam_sad.jpg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# emotion_recognition(gray)
# ## Draw a rectangle around the faces
# img = cv2.imread("webcam_normal.jpg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# emotion_recognition(gray)
# #
# img = cv2.imread("webcam_happy.jpg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# emotion_recognition(gray)
#==============================================================================
