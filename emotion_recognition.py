# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:21:55 2016

@author: Greta
"""
import cv2
#import prepare_dataset
from sklearn.externals import joblib
import getLandmark as land
model = joblib.load('svc_1.pkl')


def emotion_recognition(image):
    features = land.get_landmarks(image)
    if features!='error':
    	pred = model.predict(features)
    	print("your emotion is",pred)
    	#return prediction.prediction(image,model)
    	return pred
    else:
	print('Features didnt find')
	return 0
        
    
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
