# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:21:55 2016

@author: Greta
"""
import training
import prediction 
import cv2
import select_features
#import prepare_dataset

def emotion_recognition(image):
  
    data=select_features.data
    model=training.training(data)
    print prediction.prediction(image,model)
        
    
img = cv2.imread("smile.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

emotion_recognition(gray)
# Draw a rectangle around the faces
