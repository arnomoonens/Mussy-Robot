# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:21:55 2016

@author: Greta
"""
import cv2
#import numpy
#import prepare_dataset
from sklearn.externals import joblib
import mouth_recognition
import getLandmark as land


# ----------------------- PREDICTION ----------------------
def prediction_Fisher(im):
    #use fisher face
    im=cv2.resize(im,(350,350))
    fishface=cv2.face.createFisherFaceRecognizer()
    try:
        fishface.load("trained_emoclassifier.xml")
    except:
        print("no xlm file for fisher model")
    face=im.reshape(1,350*350)
    pred,conf=fishface.predict(face)
    print("your emotion is",pred)
    #return prediction.prediction(image,model)
    return pred

def prediction_mouth(im):
    #use svm based on mouth
    scale=1.1
    neighbors=25
    #load the model
    model = joblib.load('trainingMouth/svc_mouth.pkl')
    detected_mouth=mouth_recognition.find_mouth(im,scale,neighbors,1)
    if(detected_mouth!=[]):
        size=[40,80]
        value_predict=model.predict(detected_mouth.reshape(1, size[0] * size[1]))
        print(value_predict)
        return value_predict
    else:
        print('no mouth')
        return 0


def prediction_land(image):
    #use land
    model = joblib.load('trainingLandmark/svc_1.pkl')
    features = land.get_landmarks(image)
    if features!='error':
        value_predict=model.predict(features)
        print("your emotion is",value_predict)
        return value_predict
    else:
        print('no features')
        return 0 
# ----------------- EMOTION RECOGNITION ---------------------------

def emotion_recognition(image):
    #return prediction_land(image)
    return prediction_mouth(image)
    #return prediction_Fisher(image)


    
    
    
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
