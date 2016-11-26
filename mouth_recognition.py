# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:40:38 2016

@author: Greta
"""
import cv2

"""
given an area to be cropped, crop() returns a cropped image
"""
def crop_pre(area,image):
    #crop = image[area[1]:area[1] + 40, area[0]:area[0]+80] #img[y: y + h, x: x + w]
    crop = image[area[1]:area[1] + area[3], area[0]:area[0]+area[2]] #img[y: y + h, x: x + w]
    crop_resize=cv2.resize(crop,(80,40))
    return crop_resize
    
#Display the resulting frame
#    cv2.imshow('image', crop)
#    k = cv2.waitKey(0)
#    # When everything is done, release the capture
#    cv2.destroyAllWindows()

def crop(area,image):
    crop = image[area[1]:area[1] + area[3], area[0]:area[0]+area[2]] #img[y: y + h, x: x + w]
    return crop

def draw_rectangle(mouth,image):
    # show(mouth)
    print(mouth)
    # Draw a rectangle around the faces

    for (x, y, w, h) in mouth:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('image', image)
    k = cv2.waitKey(0)
    # When everything is done, release the capture
    cv2.destroyAllWindows()

def find_face(im):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces=faceCascade.detectMultiScale(im,scaleFactor=1.1,minNeighbors=6)
    max_face_size=0
    max_face=(0,0,0,0)

    for (x, y, w, h) in faces:
        if w*h > max_face_size:
            max_face_size=w*h
            max_face=(x,y,w,h)
    return max_face


def find_mouth(im,scale,n_nei,preprocess):
    mouthCascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
    #running classifier
    #max_face=find_face(im)
    w,h = im.shape
    max_face = (0,0,w,h)

    faceLower_h= int(max_face[3]*0.65)
    faceLower_y = max_face[1] + faceLower_h

    new_face=(max_face[0],faceLower_y,max_face[2], faceLower_h)
    faceLower=crop(new_face,im)
    #print("crop")
    #print(faceLower)
    mouths=mouthCascade.detectMultiScale(faceLower,scaleFactor=scale,minNeighbors=n_nei)

    if mouths!=():
    	#draw_rectangle(mouths[0],faceLower)
    	#print(mouths)
    	if(preprocess==1):
    	    mouth_im=crop_pre(mouths[0],faceLower)
    	else:
      	    mouth_im=crop(mouths[0],faceLower)
	return mouth_im
    else:
	print 'mouth dont find'
	return []
    


#img = cv2.imread("webcam.jpg")
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#mouth = find_mouth(gray)
## show(mouth)
#print(mouth)
#
#
## Draw a rectangle around the faces
#
#for (x, y, w, h) in mouth:
#    cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
#
#
## Display the resulting frame
#cv2.imshow('image', gray)
#k = cv2.waitKey(0)
#
#
#
## When everything is done, release the capture
#cv2.destroyAllWindows()
