# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 20:46:26 2016

@author: Greta
"""
import mouth_recognition

def prediction(im,pre_model):
    scale=1.1
    neighbors=25
    #from matplotlib.patches import Rectangle
    #ax = gca()
    #ax.imshow(im, cmap='gray')
    #detected_faces=mouth_recognition.find_face(im)
    #for (x, y, w, h) in detected_faces:
        #ax.add_artist(Rectangle((x, y), w, h, fill=False, lw=5, color='blue'))
        
    detected_mouth=mouth_recognition.find_mouth(im,scale,neighbors,1)
    size=[40,80]
    value_predict=pre_model.predict(detected_mouth.reshape(1, size[0] * size[1]))
    print(value_predict)
    return value_predict