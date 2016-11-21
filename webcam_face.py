# -*- coding: utf-8 -*-
    
import cv2
import sys
 
def web_cam():   
    #cascPath = sys.argv[1]
    #faceCascade = cv2.CascadeClassifier(cascPath)
    
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    """take image from webcam"""
    
    video_capture = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
        
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Display the resulting frame
            cv2.imshow('Video', frame)
        
            k = cv2.waitKey(10)
        
        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            break
            
        if k == 0x63 or k == 0x43:
            print 'capturing!'
            s, img = video_capture.read()
            if s:
                cv2.imwrite("test.png",img)
            # When everything is done, release the capture
            break
        video_capture.release()
            

    

web_cam()