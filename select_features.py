# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 18:30:57 2016

@author: Greta
"""
import mouth_recognition
from PIL import Image
import numpy

#values for mouthCascade.detectMultiScale for find mouths
scale=1.1
neighbors=25
    
    
im_sad=[]
im_happy=[]
im_normal=[]

mouth_sad=[]
mouth_happy=[]
mouth_normal=[]

    
    
for i in range(1,10):
    im_sad.append((numpy.asarray(Image.open("yalefaces/yalefaces/subject0"+str(i)+".sad").convert('RGB').convert("L"))))
    im_happy.append( (numpy.asarray(Image.open("yalefaces/yalefaces/subject0"+str(i)+".happy").convert('RGB').convert("L"))))
    im_normal.append( (numpy.asarray(Image.open("yalefaces/yalefaces/subject0"+str(i)+".normal").convert('RGB').convert("L"))))

for i in range(10,16):
    im_sad.append( (numpy.asarray(Image.open("yalefaces/yalefaces/subject"+str(i)+".sad").convert('RGB').convert("L"))))
    im_happy.append( (numpy.asarray(Image.open("yalefaces/yalefaces/subject"+str(i)+".happy").convert('RGB').convert("L"))))
    im_normal.append( (numpy.asarray(Image.open("yalefaces/yalefaces/subject"+str(i)+".normal").convert('RGB').convert("L"))))

for im in im_sad:
    im_mouth=mouth_recognition.find_mouth(im,scale,neighbors,1)
    mouth_sad.append(im_mouth)
    
for im in im_happy:
    im_mouth=mouth_recognition.find_mouth(im,scale,neighbors,1)
    mouth_happy.append(im_mouth)
     
for im in im_normal:
     im_mouth=mouth_recognition.find_mouth(im,scale,neighbors,1)
     mouth_normal.append(im_mouth)
size=[40,80]
    
data=(numpy.concatenate((mouth_sad,mouth_happy,mouth_normal),axis=0)).reshape(45, size[0] * size[1])




