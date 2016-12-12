import numpy as np
import cv2
from multiprocessing import Process, Queue, Lock
import time
import sys
from speech_to_text import get_voice_feedback
from text_to_speech import speak
import myservo as servo
import mysound as sound

aliveP = Queue()
aliveP.put(1)

mylock = Lock()

imageQ = Queue()

# ------- close everything --------
def exit_all():
    while not imageQ.empty():
	trash=imageQ.get()
    trash=aliveP.get() #close all process alive
    cam.release()
    cv2.destroyAllWindows()
    proc.terminate()
    proc_2.terminate()
    proc_sound.terminate()
    print 'Every thing is closed.'

# ------- function to detect the face -----
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects
# draw a rectangle on the face
def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

speak("Hello! Say 'hello mussy' to start.")
get_voice_feedback(["hello mussy"], timeout=30)  # timout seconds
print('Hi, I am here.')

# ---- initialization-----
proc = Process(target=servo.P0, args=(aliveP,))
proc_2 = Process(target=servo.P1, args=(aliveP,))
proc_sound = Process(target=sound.play, args=(aliveP, imageQ, mylock))

proc.start()
proc_2.start()
proc_sound.start()
time.sleep(.1)

# ------ main program start ------
if __name__ == '__main__':

 frontface_path = "../opencv-3.0.0/data/haarcascades/haarcascade_frontalface_alt2.xml"
 profileface_path = "../opencv-3.0.0/data/haarcascades/haarcascade_profileface.xml"
 upperbody_path = "../opencv-3.0.0/data/haarcascades/haarcascade_upperbody.xml"

 frontface = cv2.CascadeClassifier(frontface_path)
 profileface = cv2.CascadeClassifier(profileface_path)
 upperbody = cv2.CascadeClassifier(upperbody_path)

 cam = cv2.VideoCapture(0)
 cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
 cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

 try:
    while True:
	face = [0, 0, 0, 0]
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

	found = False
	frontal_found = False
	#detect the face in 3 ways
	if not found:
		rects = detect(gray, frontface)
		if rects != []:
			found = True
			frontal_found = True
	if not found:
		rects = detect(gray, profileface)
		if rects != []:
			found = True
	if not found:
                rects = detect(gray, upperbody)
                if rects != []:
                        found = True


	#we are given an x,y corner point and a width and height, we need the center
	for f in rects:
		face = f
	x, y, w, z = face
	Cface = [(w + x) / 2, (z + y) / 2]

	#add the image face on the queue for the emotion recognition
        if frontal_found:
		if imageQ.empty():
			mylock.acquire()
			print 'put'
                    	#imageQ.put(gray[y:z, x:w])
		    	imageQ.put(gray)
			mylock.release()

        #if face is found the camera follow it
	if Cface[0] != 0:
		if Cface[0] > 240:
			servo.turnR(2)
		elif Cface[0] < 140:
			servo.turnL(2)

		if Cface[1] > 180:
			servo.turnUp(1)
		elif Cface[1] < 100:
			servo.turnDw(1)

	#Show the result on the screen
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        cv2.imshow('facedetect', vis)
        if 0xFF & cv2.waitKey(5) == 27:
            exit_all()
            break

 # ----- catch the errors -----
 except IOError as (errno, strerror):
    exit_all()
    print "I/O error({0}): {1}".format(errno, strerror)
 except KeyboardInterrupt:
    exit_all()
    print 'Done.'
 except:
    exit_all()
    print "Unexpected error:", sys.exc_info()[0]
    raise
