import pigpio 
import time
from multiprocessing import Process, Queue, Lock


#----------------------- SERVO 1 ----------------------------
speed = .1
minP = 20
maxP = 160
currentP = 90
newP = 90
q = Queue() #queue for the new position
q.put(newP)
q2 = Queue() #queue for the current position
q2.put(currentP)
l = Lock()

#800 minimo fino a 1900


def g2q(g):
    return 2000./180.*(g)+500

def turnL(dist):
    global newP
    l.acquire()
    if not q.empty():
        newP = q.get()
    newP = newP+dist
    if newP > maxP:
        newP = maxP
    q.put(newP)
    l.release()
    
def turnR(dist):
    global newP
    l.acquire()
    if not q.empty():
        newP = q.get()
    newP = newP-dist
    if newP < minP:
        newP = minP
    q.put(newP)
    l.release()
    
def P0(proc):
 try:
    servoPin=23
    pi = pigpio.pi()
    _newP = 90
    while not proc.empty():
        l.acquire()
        if not q.empty():
            _newP = q.get()
        _currentP = q2.get()
        while _currentP < _newP:
            #move the motor
            _currentP += 1
            pi.set_servo_pulsewidth(servoPin,g2q(_currentP))
        while _currentP > _newP:
            #move the motor
            _currentP -= 1
            pi.set_servo_pulsewidth(servoPin,g2q(_currentP))
        q2.put(_currentP)
        l.release()
    pi.stop()
    print 'Process P0 terminated.'
 except:
     print 'Error!!Process P0 terminated:'
     pi.stop()

# ----------------------------- SERVO 2 ------------------
speed = .1
minP_2 = 40
maxP_2 = 120
currentP_2 = 90
newP_2 = 90
q_2 = Queue() #queue for the new position
q_2.put(newP_2)
q2_2 = Queue() #queue for the current position
q2_2.put(currentP_2)
l_2 = Lock()

def turnDw(dist):
    global newP_2
    l_2.acquire()
    if not q_2.empty():
        newP_2 = q_2.get()
    newP_2 = newP_2+dist
    if newP_2 > maxP_2 :
        newP_2  = maxP_2 
    q_2 .put(newP_2 )
    l_2 .release()
    
def turnUp(dist):
    global newP_2 
    l_2 .acquire()
    if not q_2 .empty():
        newP_2  = q_2 .get()
    newP_2  = newP_2 -dist
    if newP_2  < minP_2 :
        newP_2  = minP_2 
    q_2 .put(newP_2 )
    l_2 .release()

def P1(proc):
 try:
    servoPin_2=17
    pi_2 = pigpio.pi()
    _newP_2 = 90
    while not proc.empty():
        l_2.acquire()
        if not q_2.empty():
            _newP_2 = q_2.get()
        _currentP_2 = q2_2.get()
        while _currentP_2 < _newP_2:
            #move the motor
            _currentP_2 += 1
            pi_2.set_servo_pulsewidth(servoPin_2,g2q(_currentP_2))
        while _currentP_2 > _newP_2:
            #move the motor
            _currentP_2 -= 1
            pi_2.set_servo_pulsewidth(servoPin_2,g2q(_currentP_2))
        q2_2.put(_currentP_2)
        l_2.release()
    pi_2.stop()
    print 'Process P1 terminated.'
 except:
     print 'Error!!Process P1 terminated'
     pi_2.stop()


