#!/usr/bin/env python

# animations
# http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper

# How to use

# export PEPPER_IP=<...>
# python
# >>> import pepper_cmd
# >>> from pepper_cmd import *
# >>> begin()
# >>> pepper_cmd.robot.<fn>()
# >>> end()

import time
import os
import socket
import threading
import math
import random
import datetime
from datetime import datetime

import qi
from naoqi import ALProxy

# Python Image Library
from PIL import Image

laserValueList = [
  # RIGHT LASER
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg01/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg01/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg02/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg02/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg03/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg03/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg04/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg04/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg05/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg05/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg06/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg06/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg07/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg07/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg08/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg08/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg09/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg09/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg10/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg10/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg11/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg11/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg12/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg12/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg13/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg13/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg14/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg14/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg15/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg15/Y/Sensor/Value",
  # FRONT LASER
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg01/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg01/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg02/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg02/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg03/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg03/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg04/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg04/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg05/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg05/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg06/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg06/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg10/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg10/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg11/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg11/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg12/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg12/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg13/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg13/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg14/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg14/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg15/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg15/Y/Sensor/Value",
  # LEFT LASER
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg01/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg01/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg02/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg02/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg03/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg03/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg04/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg04/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg05/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg05/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg06/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg06/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg07/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg07/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg08/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg08/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg09/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg09/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg10/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg10/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg11/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg11/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg12/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg12/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg13/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg13/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg14/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg14/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg15/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg15/Y/Sensor/Value"
]


app = None
session = None
tts_service = None
memory_service = None
motion_service = None
anspeech_service = None
tablet_service = None

robot = None        # PepperRobot object

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

# Sensors
headTouch = 0.0
handTouch = [0.0, 0.0] # left, right
sonar = [0.0, 0.0] # front, back


# Sensors

def sensorThread(robot):
    sonarValues = ["Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value",
                  "Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"]
    headTouchValue = "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"
    handTouchValues = [ "Device/SubDeviceList/LHand/Touch/Back/Sensor/Value",
                   "Device/SubDeviceList/RHand/Touch/Back/Sensor/Value" ]
    frontLaserValues = [ 
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/X/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/Y/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/X/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/Y/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/X/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/Y/Sensor/Value" ]
 
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        robot.headTouch = robot.memory_service.getData(headTouchValue)
        robot.handTouch = robot.memory_service.getListData(handTouchValues)
        robot.sonar = robot.memory_service.getListData(sonarValues)
        laserValues = robot.memory_service.getListData(frontLaserValues)
        dd = 0 # average distance
        c = 0        
        for i in range(0,len(laserValues),2):
            px = laserValues[i] if laserValues[i] is not None else 10
            py = laserValues[i+1] if laserValues[i+1] is not None else 0
            d = math.sqrt(px*px+py*py)
            if d<10:
                dd = dd + d
                c = c+1
        
        if (c>0):
            robot.frontlaser = dd / c
        else:
            robot.frontlaser = 10.0

        #print "Head touch middle value=", robot.headTouch
        #print "Hand touch middle value=", robot.handTouch
        #print "Sonar [Front, Back]", robot.sonar
        time.sleep(0.2)
    #print "Exiting Thread"




def touchcb(value):
    print "value=",value

    touched_bodies = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])

    print touched_bodies

asr_word = ''
asr_confidence = 0
asr_timestamp = 0

def onWordRecognized(value):
    global asr_word, asr_confidence, asr_timestamp
    print "ASR value = ",value,time.time()
    if (value[1]>0 and value[0]!=''):
    #if (value[1]>0 and (value[0]!='' or time.time()-asr_timestamp>1.0)):
    #if (value[1]>0):
        asr_word = value[0]
        asr_confidence = value[1]
        asr_timestamp = time.time()

def sensorvalue(sensorname):
    global robot
    if (robot!=None):
        return robot.sensorvalue(sensorname)


touchcnt = 0

# function called when the signal onTouchDown is triggered
def touch_cb(x, y):
    global robot, touchcnt
    print "Touch coordinates are x: ", x, " y: ", y
    robot.screenTouch = (x,y)
    touchcnt = touchcnt + 1
    time.sleep(1)
    touchcnt = touchcnt - 1
    if touchcnt == 0:
        robot.screenTouch = (0.0,0.0)



def laserMonitorThread (memory_service):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        laserValues =  memory_service.getListData(laserValueList)
        #print laserValues[44],laserValues[45] #X,Y values of central point
        time.sleep(0.2)
    print "Exiting Thread"


# Begin/end

def begin():
    global robot
    print 'begin'
    if (robot==None):
        robot=PepperRobot()
        robot.connect()
    robot.begin()

def end():
    global robot
    print 'end'
    time.sleep(0.5) # make sure stuff ends
    if (robot!=None):
        robot.quit()


# Robot motion

def stop():
    global robot
    if (robot==None):
        begin()
    robot.stop()

def forward(r=1):
    global robot
    if (robot==None):
        begin()
    robot.forward(r)

def backward(r=1):
    global robot
    if (robot==None):
        begin()
    robot.backward(r)

def left(r=1):
    global robot
    if (robot==None):
        begin()
    robot.left(r)

def right(r=1):
    global robot
    if (robot==None):
        begin()
    robot.right(r)

def robot_stop_request(): # stop until next begin()
    if (robot!=None):
        robot.stop_request = True
        robot.stop()
        print("stop request")



# Wait

def wait(r=1):
    print 'wait',r
    for i in range(0,r):
        time.sleep(3)


# Sounds

def bip(r=1):
    print 'bip'


def bop(r=1):
    print 'bop'


# Speech

def say(strsay):
    global robot
    print 'Say ',strsay
    if (robot==None):
        begin()
    robot.say(strsay)

def asay(strsay):
    global robot
    print 'Animated Say ',strsay
    if (robot==None):
        begin()
    robot.asay(strsay)



# Other 

# Alive behaviors
def setAlive(alive):
    global robot
    robot.setAlive(alive)

def stand():
    global robot
    robot.stand()

def disabled():
    global robot
    robot.disabled()

def interact():
    global robot
    robot.interactive()


def showurl(url):
    global robot
    if (robot!=None):
        return robot.showurl(url)


def run_behavior(bname):
    global session
    beh_service = session.service("ALBehaviorManager")
    beh_service.startBehavior(bname)
    #time.sleep(10)
    #beh_service.stopBehavior(bname)


def takephoto():
    global robot
    robot.takephoto()


def opendiag():
    global robot
    robot.introduction()

def sax():
    global robot
    robot.sax()


class PepperRobot:

    def __init__(self):
        self.isConnected = False
        # Sensors
        self.headTouch = 0.0
        self.handTouch = [0.0, 0.0] # left, right
        self.sonar = [0.0, 0.0] # front, back
        self.frontlaser = 0.0
        self.screenTouch = (0,0)
        self.language = "English"
        self.stop_request = False
        self.frame_grabber = False
        self.face_detection = False
        self.got_face = False

        self.FER_server_IP = None
        self.FER_server_port = 5678

        self.logfile = None

        self.sensorThread = None
        self.laserThread = None
        self.lthr = None # log thread

        self.jointNames = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]

        self.fakeASRkey = 'FakeRobot/ASR'
        self.fakeASRtimekey = 'FakeRobot/ASRtime'


    def session_service(self,name):
        try:
            return self.session.service(name)
        except:
            print("Service %s not available." %(name))
            return None


    # Connect to the robot
    def connect(self, pip=os.environ['PEPPER_IP'], pport=None, alive=False):

        self.ip = pip
        if pport is not None:
            self.port = pport
        elif 'PEPPER_PORT' in os.environ:
            self.port = int(os.environ['PEPPER_PORT'])
        else:
            self.port = 9559

        if (self.isConnected):
            print("Robot already connnected.")
            return

        print("Connecting to robot %s:%d ..." %(self.ip,self.port))
        try:
            connection_url = "tcp://" + self.ip + ":" + str(self.port)
            self.app = qi.Application(["Pepper command", "--qi-url=" + connection_url ])
            self.app.start()
        except RuntimeError:
            print("%sCannot connect to Naoqi at %s:%d %s" %(RED,self.ip,self.port,RESET))
            self.session = None
            return

        print("%sConnected to robot %s:%d %s" %(GREEN,self.ip,self.port,RESET))
        self.session = self.app.session

        print("Starting services...")

        #Starting services
        self.memory_service  = self.session.service("ALMemory")
        self.motion_service  = self.session.service("ALMotion")
        self.tts_service = self.session.service("ALTextToSpeech")
        self.anspeech_service = self.session.service("ALAnimatedSpeech")
        self.leds_service = self.session.service("ALLeds")
        self.asr_service = None
        self.tablet_service = None
        self.bm_service = None
        try:
            self.asr_service = self.session.service("ALSpeechRecognition")
            self.tablet_service = self.session.service("ALTabletService")
            self.touch_service = self.session.service("ALTouch")
            self.animation_player_service = self.session.service("ALAnimationPlayer")
            self.beh_service = self.session.service("ALBehaviorManager")
            self.al_service = self.session.service("ALAutonomousLife")
            self.rp_service = self.session.service("ALRobotPosture")
            self.bm_service = self.session.service("ALBackgroundMovement")
            self.ba_service = self.session.service("ALBasicAwareness")
            self.sm_service = self.session.service("ALSpeakingMovement")
            self.audiorec_service = self.session.service("ALAudioRecorder")
            self.audio_service = self.session.service("ALAudioDevice")
            self.battery_service = self.session.service("ALBattery")
            self.people_service = self.session.service("ALPeoplePerception")

        except:
            pass

        if self.bm_service!=None:
            self.alive = alive
            print('Alive behaviors: %r' %self.alive)
            if self.bm_service!=None:
                self.bm_service.setEnabled(self.alive)
            if self.ba_service!=None:
                self.ba_service.setEnabled(self.alive)
            if self.sm_service!=None:
                self.sm_service.setEnabled(self.alive)
            
        if self.tablet_service!=None:
            webview = "http://198.18.0.1/apps/spqrel/index.html"
            self.tablet_service.showWebview(webview)
            self.touchsignalID = self.tablet_service.onTouchDown.connect(touch_cb)
            self.touchstatus = self.touch_service.getStatus()
            #print touchstatus
            self.touchsensorlist = self.touch_service.getSensorList()
            #print touchsensorlist


        self.isConnected = True


    def quit(self):
        print "Quit Pepper robot."
        self.sensorThread = None
        self.laserThread = None
        if self.sensorThread != None:
            self.sensorThread.do_run = False
            self.sensorThread = None
        if self.laserThread != None:
            self.laserThread.do_run = False
            self.laserThread = None
        
        if self.session!=None and self.tablet_service!=None:
            self.tablet_service.onTouchDown.disconnect(self.touchsignalID)
        time.sleep(1)
        self.app.stop()
        

    # general commands

    def begin(self):
        self.stop_request = False
        self.ears_led(False)
        self.white_eyes()

    def exec_cmd(self, params):
        cmdstr = "self."+params
        print "Executing %s" %(cmdstr)
        eval(cmdstr)    

    def tablet_home(self):
        webview = "http://198.18.0.1/apps/spqrel/index.html"
        self.tablet_service.showWebview(webview)


    # Network

    def networkstatus(self):
        # TODO
        #self.tablet_service.configureWifi(const std::string& security, const std::string& ssid, const std::string& key)
        #connectWifi(const std::string& ssid)
        return self.tablet_service.getWifiStatus()


    def robotIp(self):
        return self.tablet_service.robotIp() # just tablet IP ...

    # Leds

    def white_eyes(self):
        # white face leds
        self.leds_service.on('FaceLeds')


    def green_eyes(self):
        if self.leds_service!=None:
            # green face leds
            self.leds_service.on('LeftFaceLedsGreen')
            self.leds_service.off('LeftFaceLedsRed')
            self.leds_service.off('LeftFaceLedsBlue')
            self.leds_service.on('RightFaceLedsGreen')
            self.leds_service.off('RightFaceLedsRed')
            self.leds_service.off('RightFaceLedsBlue')

    def red_eyes(self):
        if self.leds_service!=None:
            # red face leds
            self.leds_service.off('LeftFaceLedsGreen')
            self.leds_service.on('LeftFaceLedsRed')
            self.leds_service.off('LeftFaceLedsBlue')
            self.leds_service.off('RightFaceLedsGreen')
            self.leds_service.on('RightFaceLedsRed')
            self.leds_service.off('RightFaceLedsBlue')

    def blue_eyes(self):
        if self.leds_service!=None:
            # red face leds
            self.leds_service.off('LeftFaceLedsGreen')
            self.leds_service.off('LeftFaceLedsRed')
            self.leds_service.on('LeftFaceLedsBlue')
            self.leds_service.off('RightFaceLedsGreen')
            self.leds_service.off('RightFaceLedsRed')
            self.leds_service.on('RightFaceLedsBlue')


    def ears_led(self, enable):
        # Ears leds
        if enable:
            self.leds_service.on('EarLeds')
        else:
            self.leds_service.off('EarLeds')


    # Touch/distance sensors

    def startSensorMonitor(self):
        if self.sensorThread == None:
            # create a thead that monitors directly the signal
            self.sensorThread = threading.Thread(target = sensorThread, args = (self, ))
            self.sensorThread.start()
            time.sleep(0.5)

    def stopSensorMonitor(self):
        self.sensorThread.do_run = False
        self.sensorThread = None


    # Laser

    def startLaserMonitor(self):
        if self.laserThread==None:
            #create a thead that monitors directly the signal
            self.laserThread = threading.Thread(target = laserMonitorThread, args = (self.memory_service,))
            self.laserThread.start()

    def stopLaserMonitor(self):
        self.laserThread.do_run = False
        self.laserThread = None


    # Camera

    def startFrameGrabber(self):
        # Connect to camera
        self.camProxy = ALProxy("ALVideoDevice", self.ip, self.port)
        resolution = 2    # VGA
        colorSpace = 11   # RGB
        # self.videoClient = self.camProxy.subscribe("grab3_images", resolution, colorSpace, 5)
        self.videoClient = self.camProxy.subscribeCamera("grab3_images", 0, resolution, colorSpace, 5)
        self.frame_grabber = True

    def stopFrameGrabber(self):
        # Connect to camera
        self.camProxy.unsubscribe(self.videoClient)
        self.frame_grabber = False

    def sendImage(self, ip, port):
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        img = self.camProxy.getImageRemote(self.videoClient)

        if img is None:
            return 'ERROR'

        # Get the image size and pixel array.
        imageWidth = img[0]
        imageHeight = img[1]
        imageArray = img[6]

        # Create a PIL Image from our pixel array.
        imx = Image.frombytes("RGB", (imageWidth, imageHeight), imageArray)

        # Convert to grayscale
        img = imx.convert('L')   
        aimg = img.tobytes()

        #print("Connecting to %s:%d ..." %(ip,port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip,port))
            #print("OK")

            #print("Sending image ...")
            #print("Image size: %d %d" %(imageWidth * imageHeight, len(aimg)))

            msg = '%9d\n' %len(aimg)
            s.send(msg.encode())
            s.send(aimg)

            data = s.recv(80)
            rcv_msg = data.decode()
            #print("Reply: %s" %rcv_msg)

            s.close()
            #print("Connection closed ")
            return rcv_msg
        except:
            print("Send image: connection error")
            return 'ERROR'


    def saveImage(self, filename):

        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        img = self.camProxy.getImageRemote(self.videoClient)

        # Get the image size and pixel array.
        imageWidth = img[0]
        imageHeight = img[1]
        imageArray = img[6]

        # Create a PIL Image from our pixel array.
        imx = Image.frombytes("RGB", (imageWidth, imageHeight), imageArray)

        # Save the image.
        imx.save(filename, "PNG")


    def startFaceDetection(self):
        if self.face_detection:  # already active
            return

        # Connect to camera
        self.startFrameGrabber()

        # Connect the event callback.
        self.frsub = self.memory_service.subscriber("FaceDetected")
        self.ch1 = self.frsub.signal.connect(self.on_facedetected)
        self.got_face = False
        self.savedfaces = []
        self.face_detection = True
        self.face_recording = False # if images are saved on file


    def stopFaceDetection(self):
        self.frsub.signal.disconnect(self.ch1)
        self.camProxy.unsubscribe(self.videoClient)
        self.face_recording = False
        self.face_detection = False
        self.white_eyes()


    def setFaceRecording(self,enable):
         self.face_recording = enable


    def on_facedetected(self, value):
        """
        Callback for event FaceDetected.
        """
        faceID = -1

        if value == []:  # empty value when the face disappears
            self.got_face = False
            self.facetimeStamp = None
            self.white_eyes()
            self.memset('facedetected', 'false')
        elif not self.got_face:  # only the first time a face appears
            self.got_face = True
            self.green_eyes()
            self.memset('facedetected', 'true')

            #print "I saw a face!"
            #self.tts.say("Hello, you!")
            self.facetimeStamp = time.time() #value[0]
            #print "TimeStamp is: " + str(self.facetimeStamp)

            # Second Field = array of face_Info's.
            faceInfoArray = value[1]
            for j in range( len(faceInfoArray)-1 ):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]

                faceID = faceExtraInfo[0]

                #print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                #print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                #print "Face Extra Infos :" + str(faceExtraInfo)

                #print "Face ID: %d" %faceID

        if self.camProxy!=None and faceID>=0 and faceID not in self.savedfaces and self.face_recording:
            # Get the image
            img = self.camProxy.getImageRemote(self.videoClient)

            # Get the image size and pixel array.
            imageWidth = img[0]
            imageHeight = img[1]
            array = img[6]

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

            # Save the image.
            fname = "face_%03d.png" %faceID
            im.save(fname, "PNG")
            print "Image face %d saved." %faceID

            self.savedfaces.append(faceID)

    # Time of continuous face detection
    def faceDetectionTime(self):
        if self.facetimeStamp is not None:
            return time.time() - self.facetimeStamp
        else:
            return 0

    # Audio settings

    def getVolume(self):
        return self.audio_service.getOutputVolume()

    def setVolume(self, v):
        self.audio_service.setOutputVolume(v)


    def timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    # Audio recording

    def startAudioRecording(self):
        audiofile = '/home/nao/audio/audiorec_%s.wav' %(datetime.now().strftime("%Y%m%d_%H%M%S"))

        # Configures the channels that need to be recorded.
        channels = [0,0,1,0]  # Left, Right, Front, Rear
        self.audiorec_service.startMicrophonesRecording(audiofile, 'wav', 16000, channels)
        self.ears_led(True)

    def stopAudioRecording(self):
        self.audiorec_service.stopMicrophonesRecording()
        self.ears_led(False)



    # Speech

    # English, Italian, French
    def setLanguage(self, lang):
        languages = {"en" : "English", "it": "Italian"}
        if  (lang in languages.jointValues()):
            lang = languages[lang]
        self.tts_service.setLanguage(lang)

    def tts(self, interaction):
        if self.stop_request:
            return
        self.tts_service.setParameter("speed", 80)
        self.tts_service.say(interaction)

    def say(self, interaction):
        if self.stop_request:
            return
        print('Say: %s' %interaction)
        if self.tts_service!=None:
            self.tts_service.setParameter("speed", 80)
            self.asay2(interaction)
 
    def asay2(self, interaction):
        if self.stop_request:
            return
        if self.anspeech_service!=None:
            # set the local configuration
            configuration = {"bodyLanguageMode":"contextual"}
            self.anspeech_service.say(interaction, configuration)

    def asay(self, interaction):
        if self.stop_request:
            return
        if self.anspeech_service is None:
            return

        # set the local configuration
        #configuration = {"bodyLanguageMode":"contextual"}

        # http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper
        vanim = ["animations/Stand/Gestures/Enthusiastic_4",
                 "animations/Stand/Gestures/Enthusiastic_5",
                 "animations/Stand/Gestures/Excited_1",
                 "animations/Stand/Gestures/Explain_1" ]
        anim = random.choice(vanim) # random animation

        if ('hello' in interaction):
            anim = "animations/Stand/Gestures/Hey_1"
    
        self.anspeech_service.say("^start("+anim+") " + interaction+" ^wait("+anim+")")


    def reset_fake_asr(self):
        self.memory_service.insertData(self.fakeASRkey,'')

    def fake_asr(self):
        global asr_word, asr_confidence, asr_timestamp
        try:
            r = self.memory_service.getData(self.fakeASRkey)
            if r!='':
                asr_word = r
                asr_confidence = 1.0
                asr_timestamp = self.memory_service.getData(self.fakeASRtimekey)
                print('fake ASR: [%s], %r' %(asr_word,asr_timestamp))
                self.reset_fake_asr()
        except:
            pass


    def asr_cancel(self):
        self.asr_cancel_flag = True

    # vocabulary = list of keywords, e.g. ["yes", "no", "please"]
    # blocking until timeout
    def asr(self, vocabulary, timeout=5):
        global asr_word, asr_confidence, asr_timestamp
        #establishing vocabulary
        if (self.asr_service != None):
            self.asr_service.pause(True)
            self.asr_service.setVocabulary(vocabulary, False)
            self.asr_service.pause(False)
            # Start the speech recognition engine with user Test_ASR
            self.asr_service.subscribe("asr_pepper_cmd")
            print 'Speech recognition engine started'

            #subscribe to event WordRecognized
            subWordRecognized = self.memory_service.subscriber("WordRecognized")
            idSubWordRecognized = subWordRecognized.signal.connect(onWordRecognized)
        else:
            print('ASR service not available. Use %s memory key to say something' %self.fakeASRkey)
            self.reset_fake_asr()
            #val = raw_input('Enter ASR text: ')
            #return val


        self.asr_cancel_flag = False
        asr_word = ''
        i = 0
        dt = 0.5
        while ((timeout<0 or i<timeout) and asr_word=='' and not self.asr_cancel_flag):
            self.fake_asr()
            time.sleep(dt)
            i += dt

        if (self.asr_service != None):
            #Disconnecting callbacks and subscribers
            self.asr_service.unsubscribe("asr_pepper_cmd")
            subWordRecognized.signal.disconnect(idSubWordRecognized)

        

        dt = time.time() - asr_timestamp

        print("dt %r %r  -  %f %f" %(time.time(),asr_timestamp, dt, timeout))

        if ((timeout<0 or dt<timeout) and asr_confidence>0.3):
            print("ASR: %s" %asr_word)
            return asr_word
        else:
            print("ASR: none")
            return ''


    def bip(self, r=1):
        print 'bip -- NOT IMPLEMENTED'


    def bop(self, r=1):
        print 'bop -- NOT IMPLEMENTED'


    # animations/Stand/Gestures/
    # Please_1
    # Hey_1; Hey_3; Hey_4
    def animation(self, interaction):
        if self.stop_request:
            return
        if interaction[0:4]!='anim':
            interaction = 'animations/Stand/Gestures/' + interaction
        print 'Animation ',interaction
        self.bm_service.setEnabled(False)
        self.ba_service.setEnabled(False)
        self.sm_service.setEnabled(False)

        try:
            self.animation_player_service.run(interaction)
        except:
            print("Error in executing gesture %s" %interaction)

        self.bm_service.setEnabled(self.alive)
        self.ba_service.setEnabled(self.alive)
        self.sm_service.setEnabled(self.alive)

    # Alive behaviors

    def setAlive(self, alive):
        if self.bm_service!=None:
            self.alive = alive
            print('Alive behaviors: %r' %self.alive)
            self.bm_service.setEnabled(self.alive)
            self.ba_service.setEnabled(self.alive)
            self.sm_service.setEnabled(self.alive)

    # Tablet

    def showurl(self, weburl):
        if self.tablet_service!=None:
            if weburl[0:4]!='http':
                weburl = "http://198.18.0.1/apps/spqrel/%s" %(weburl)
            print("URL: %s" %weburl)
            if weburl[-3:]=='jpg' or weburl[-3:]=='png':
                self.tablet_service.showImage(weburl)
            else:
                self.tablet_service.showWebview(weburl)


    # Robot motion

    def stop(self):
        print 'stop'
        self.motion_service.stopMove()
        if self.beh_service!=None:
            bns = self.beh_service.getRunningBehaviors()
            for b in bns:
                self.beh_service.stopBehavior(b)

    def forward(self, r=1):
        if self.stop_request:
            return
        print 'forward',r
        x = r
        y = 0.0
        theta = 0.0
        self.motion_service.moveTo(x, y, theta) #blocking function

    def backward(self, r=1):
        if self.stop_request:
            return
        print 'backward',r
        x = -r
        y = 0.0
        theta = 0.0
        self.motion_service.moveTo(x, y, theta) #blocking function

    def left(self, r=1):
        if self.stop_request:
            return
        print 'left',r
        #Turn 90deg to the left
        x = 0.0
        y = 0.0
        theta = math.pi/2 * r
        self.motion_service.moveTo(x, y, theta) #blocking function

    def right(self, r=1):
        if self.stop_request:
            return
        print 'right',r
        #Turn 90deg to the right
        x = 0.0
        y = 0.0
        theta = -math.pi/2 * r
        self.motion_service.moveTo(x, y, theta) #blocking function

    def turn(self, r):
        if self.stop_request:
            return
        print 'turn',r
        #Turn r deg
        vx = 0.0
        vy = 0.0
        vth = r * math.pi / 180 
        self.motion_service.moveTo(vx, vy, vth) #blocking function

    def setSpeed(self,vx,vy,vth,tm,stopOnEnd=False):
        if self.stop_request:
            return
        self.motion_service.move(vx, vy, vth)
        time.sleep(tm)
        if stopOnEnd:
            self.motion_service.move(0, 0, 0)
            self.motion_service.stopMove()
            

    def think(self):
    
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.3, 1.2, 2.48])
	keys.append([-0.377539, -0.377539, 0.211185])

	names.append("HeadYaw")
	times.append([0.3, 1.2, 2.48])
	keys.append([0.00912633, 0.00912633, -0.221657])

	names.append("HipPitch")
	times.append([0.3, 1.2, 2.48])
	keys.append([-0.0426928, -0.0426927, -0.118682])

	names.append("HipRoll")
	times.append([0.3, 1.2, 2.48])
	keys.append([-0.00887858, -0.00887858, 0.0610865])

	names.append("KneePitch")
	times.append([0.3, 1.2])
	keys.append([-0.00663467, -0.00663468])

	names.append("LElbowRoll")
	times.append([0.3, 1.2, 2.48, 3.08])
	keys.append([-0.108104, -0.764454, -1.56207, -1.46433])

	names.append("LElbowYaw")
	times.append([0.3, 1.2, 2.48, 3.08])
	keys.append([-1.71638, -1.80467, -0.450295, -0.640536])

	names.append("LHand")
	times.append([0.3, 1.2, 2.48, 3.08, 3.52, 3.76, 4])
	keys.append([0.6942, 0.6942, 0.39, 0.82, 0.05, 0.8, 0.05])

	names.append("LShoulderPitch")
	times.append([0.4, 1.2, 2.48, 3.08, 3.28])
	keys.append([1.77271, 1.00706, -1.49051, -1.23569, -1.28631])

	names.append("LShoulderRoll")
	times.append([0.3, 1.2, 2.48])
	keys.append([0.103651, 0.103651, 0.407583])

	names.append("LWristYaw")
	times.append([0.3, 1.2, 2.48, 3.08])
	keys.append([0.0425655, 0.0425654, -0.527089, -1.19206])

	names.append("RElbowRoll")
	times.append([0.3, 1.2])
	keys.append([0.102232, 0.102232])

	names.append("RElbowYaw")
	times.append([0.3, 1.2])
	keys.append([1.69033, 1.69033])

	names.append("RHand")
	times.append([0.3, 1.2])
	keys.append([0.688049, 0.688049])

	names.append("RShoulderPitch")
	times.append([0.3, 1.2])
	keys.append([1.75191, 1.75191])

	names.append("RShoulderRoll")
	times.append([0.3, 1.2])
	keys.append([-0.102647, -0.102647])

	names.append("RWristYaw")
	times.append([0.3, 1.2])
	keys.append([-0.0258008, -0.0258009])


	self.motion_service.angleInterpolation(names, keys, times, True)
	self.normalPosture()

    
    def hello(self):
    
        isAbsolute = True
    
        jointNames = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", 	"RWristYaw"]
        jointValues = [1.32, 1.42, 1.71, -0.03, -0.10, -1.01]
        times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        
        self.motion_service.angleInterpolation(jointNames, jointValues, times, isAbsolute)

        self.motion_service.angleInterpolation("RElbowYaw", 1.83, 0.8, isAbsolute)

        self.motion_service.angleInterpolation("RElbowYaw", 1.04, 0.8, isAbsolute)

        self.motion_service.angleInterpolation("RElbowYaw", 1.42, 0.8, isAbsolute)
        
        self.normalPosture()
        
    def showTablet(self):
     
        isAbsolute = True
        
	names = list()
	times = list()
	keys = list()

	names.append("LElbowRoll")
	times.append([0.3, 0.7, 1.2])
	keys.append([-0.325779, -1.24861, -1.52963])

	names.append("LElbowYaw")
	times.append([0.3, 0.7 , 1.2])
	keys.append([-0.943899, -1.60194, -0.252625])

	names.append("LHand")
	times.append([0.3, 0.7, 1.2])
	keys.append([0.353481, 0.519131, 0.836042])

	names.append("LShoulderPitch")
	times.append([0.3, 0.7,  1.2])
	keys.append([1.50993, 0.569389, -0.14717])

	names.append("LShoulderRoll")
	times.append([0.3, 0.7, 1.2])
	keys.append([0.216273, 0.623649, 0.703776])

	names.append("LWristYaw")
	times.append([0.3, 0.7, 1.2])
	keys.append([-0.4881, -0.478707, -0.603625])

	names.append("RElbowRoll")
	times.append([0.3, 0.7, 1.2])
	keys.append([0.458528, 1.23183, 1.44387])

	names.append("RElbowYaw")
	times.append([0.3, 0.7, 1.2])
	keys.append([0.890075, 1.6116, 0.511499])

	names.append("RHand")
	times.append([0.3, 0.7, 1.2])
	keys.append([0.372075, 0.536579, 0.789008])

	names.append("RShoulderPitch")
	times.append([0.3, 0.7, 1.2])
	keys.append([1.2999, 1.49751, 0.960532])

	names.append("RShoulderRoll")
	times.append([0.3, 0.7, 1.2])
	keys.append([-0.206746, -0.560627, -0.701282])

	names.append("RWristYaw")
	times.append([0.3, 0.7, 1.2])
	keys.append([0.565597, 0.556715, 1.66671])


	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say('This is the tablet, you have to look here')
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()
	
	time.sleep(1)
	self.normalPosture()
	
	
    def intro(self):
    
    	isAbsolute=True
    	
    	#OpenArmInFront
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.48, 0.84])
	keys.append([-0.192183, -0.368462])

	names.append("HeadYaw")
	times.append([0.84])
	keys.append([0])

	names.append("HipPitch")
	times.append([0.56, 1])
	keys.append([-0.309665, -0.065382])

	names.append("HipRoll")
	times.append([0.56, 1])
	keys.append([-0.0079017, -0.0079017])

	names.append("KneePitch")
	times.append([0.56, 1])
	keys.append([0.205769, 0.0608205])

	names.append("LElbowRoll")
	times.append([0.56, 0.92])
	keys.append([-1.00013, -0.414292])

	names.append("LElbowYaw")
	times.append([0.56, 0.92])
	keys.append([-1.56462, -1.78575])

	names.append("LHand")
	times.append([0.56, 0.92])
	keys.append([0.3168, 0.72])

	names.append("LShoulderPitch")
	times.append([0.56, 0.92])
	keys.append([0.918823, 0.802022])

	names.append("LShoulderRoll")
	times.append([0.56, 0.92])
	keys.append([0.382278, 0.492623])

	names.append("LWristYaw")
	times.append([0.56, 0.92])
	keys.append([-0.937315, -1.22341])

	names.append("RElbowRoll")
	times.append([0.48, 0.84])
	keys.append([1.08918, 0.415538])

	names.append("RElbowYaw")
	times.append([0.48, 0.84])
	keys.append([1.64636, 1.74221])

	names.append("RHand")
	times.append([0.48, 0.84])
	keys.append([0.024, 0.72])

	names.append("RShoulderPitch")
	times.append([0.48, 0.84])
	keys.append([0.570689, 0.487636])

	names.append("RShoulderRoll")
	times.append([0.48, 0.84])
	keys.append([-0.237621, -0.367388])

	names.append("RWristYaw")
	times.append([0.48, 0.84])
	keys.append([0.793036, 1.2251])
	
	
	#self.motion_service.moveInit()
	#self.motion_service.angleInterpolation(names, keys, times, isAbsolute)
	#self.say('This is my friend, Marco')
	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say("This is my friend, Marco")
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()

	#LittleSpreadRightArms
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([1.12, 1.8, 2.16])
	keys.append([-0.205769, -0.370226, -0.293631])

	names.append("HeadYaw")
	times.append([0.2, 0.56, 0.84, 1.12, 1.4, 1.72, 2.16])
	keys.append([-0.0122965, -0.0102073, -0.0985437, 0.0893026, -0.0985437, 0.0893026, -0.0140261])

	names.append("HipPitch")
	times.append([0.76, 2.16])
	keys.append([-0.187014, -0.05314])

	names.append("HipRoll")
	times.append([0.76, 2.16])
	keys.append([-0.0456695, -0.0456695])

	names.append("KneePitch")
	times.append([0.76, 2.16])
	keys.append([0.0811503, -0.00708406])

	names.append("LElbowRoll")
	times.append([1.12, 1.8, 2.16])
	keys.append([-0.425288, -0.418776, -0.416156])

	names.append("LElbowYaw")
	times.append([1.12, 1.8, 2.16])
	keys.append([-1.43356, -1.19957, -1.19838])

	names.append("LHand")
	times.append([1.12, 1.8, 2.16])
	keys.append([0.84, 0.311072, 0.306419])

	names.append("LShoulderPitch")
	times.append([1.12, 1.8, 2.16])
	keys.append([1.40624, 1.45575, 1.46352])

	names.append("LShoulderRoll")
	times.append([1.12, 1.8, 2.16])
	keys.append([0.358248, 0.242796, 0.206013])

	names.append("LWristYaw")
	times.append([1.12, 1.8, 2.16])
	keys.append([-0.656244, 0.076658, 0.0977037])

	names.append("RElbowRoll")
	times.append([0.92, 1.6, 2.04])
	keys.append([0.428422, 0.421844, 0.413016])

	names.append("RElbowYaw")
	times.append([0.92, 1.6, 2.04])
	keys.append([2.03783, 1.32996, 1.19382])

	names.append("RHand")
	times.append([0.92, 1.6, 2.04])
	keys.append([0.85, 0.351494, 0.3])

	names.append("RShoulderPitch")
	times.append([0.92, 1.6, 2.04])
	keys.append([1.4546, 1.45882, 1.46675])

	names.append("RShoulderRoll")
	times.append([0.92, 1.6, 2.04])
	keys.append([-0.3529, -0.330302, -0.267505])

	names.append("RWristYaw")
	times.append([0.92, 1.6, 2.04])
	keys.append([0.783567, 0.216252, 0.108709])
	
	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say("Marco is not able to hear sounds and to speak")
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()
	
	#RightArmUpAndDown
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.44, 0.96, 1.48, 2.32, 2.8])
	keys.append([-0.515251, -0.34076, -0.0929187, -0.257377, -0.329649])

	names.append("HeadYaw")
	times.append([0.44, 0.96, 1.24, 1.48, 1.8, 2.12, 2.48, 2.8])
	keys.append([-0.0156179, -0.0135287, -0.12827, 0.0965434, -0.12827, 0.0965434, -0.0173475, -0.0123995])

	names.append("HipPitch")
	times.append([0.44, 0.96, 2.32])
	keys.append([-0.158713, -0.0544052, -0.277851])

	names.append("HipRoll")
	times.append([0.44, 0.96, 2.32])
	keys.append([-0.0168668, 0.0440326, 0.00417265])

	names.append("KneePitch")
	times.append([0.44, 0.96, 2.32])
	keys.append([0.0375921, -0.0223025, 0.0887257])

	names.append("LElbowRoll")
	times.append([0.44, 0.96, 1.88, 2.8])
	keys.append([-0.425005, -0.68766, -0.425288, -0.416156])

	names.append("LElbowYaw")
	times.append([0.44, 0.96, 1.8, 2.8])
	keys.append([-1.39032, -1.9088, -1.96299, -1.45377])

	names.append("LHand")
	times.append([0.44, 0.96, 1.88, 2.8])
	keys.append([0.305394, 0.62, 0.314203, 0.306419])

	names.append("LShoulderPitch")
	times.append([0.44, 0.96, 1.88, 2.8])
	keys.append([1.41011, 1.45418, 1.40624, 1.46352])

	names.append("LShoulderRoll")
	times.append([0.44, 0.96, 1.88, 2.8])
	keys.append([0.241407, 0.44927, 0.246933, 0.18874])

	names.append("LWristYaw")
	times.append([0.44, 0.96, 1.88, 2.8])
	keys.append([-0.111101, -0.111101, -0.108112, 0.0977037])

	names.append("RElbowRoll")
	times.append([0.44, 0.72, 1.24, 1.88, 2.8])
	keys.append([0.431716, 0.429253, 0.998328, 0.428422, 0.413016])

	names.append("RElbowYaw")
	times.append([0.44, 0.96, 1.48, 1.88, 2.8])
	keys.append([1.21446, 2.02109, 2.02008, 1.91888, 1.19382])

	names.append("RHand")
	times.append([0.44, 0.96, 1.24, 1.48, 1.88, 2.8])
	keys.append([0.315043, 0.98, 0.98, 0.65, 0.53724, 0.3])

	names.append("RShoulderPitch")
	times.append([0.44, 0.96, 1.48, 1.88, 2.8])
	keys.append([1.41886, 1.14145, 1.42942, 1.4546, 1.46675])

	names.append("RShoulderRoll")
	times.append([0.44, 0.96, 1.48, 1.88, 2.8])
	keys.append([-0.194604, -0.212728, -0.211925, -0.204261, -0.181265])

	names.append("RWristYaw")
	times.append([0.44, 0.96, 1.48, 1.88, 2.8])
	keys.append([-0.0875347, 0.912807, 0.90059, 0.783567, 0.108709])
	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say("He often feels sad because it's very hard for him to make friends")
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()
	


	#StrongArmOpen
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.52, 1.04, 1.48])
	keys.append([-0.415657, -0.123426, -0.369636])

	names.append("HeadYaw")
	times.append([0.52, 1.04, 1.48])
	keys.append([0.0398422, 0.0398422, 0.0536479])

	names.append("HipPitch")
	times.append([0.4, 0.72, 0.84, 1.28, 1.48])
	keys.append([-0.120399, -0.178497, -0.235035, -0.104673, -0.0659148])

	names.append("HipRoll")
	times.append([0.4, 0.72, 0.84, 1.28, 1.48])
	keys.append([-0.022229, -0.022229, -0.022229, -0.0122608, -0.0016941])

	names.append("KneePitch")
	times.append([0.4, 0.72, 0.84, 1.28, 1.48])
	keys.append([0.0319777, 0.0964101, 0.133068, 0.0460924, 0.0185926])

	names.append("LElbowRoll")
	times.append([0.36, 0.96, 1.44])
	keys.append([-1.01055, -1.15715, -1.30027])

	names.append("LElbowYaw")
	times.append([0.36, 0.96, 1.44])
	keys.append([-1.15054, -1.71812, -1.77181])

	names.append("LHand")
	times.append([0.36, 0.96, 1.44])
	keys.append([0.2132, 0.68, 0.7728])

	names.append("LShoulderPitch")
	times.append([0.36, 0.96, 1.44])
	keys.append([1.333, 1.32687, 1.2706])

	names.append("LShoulderRoll")
	times.append([0.36, 0.96, 1.44])
	keys.append([0.132418, 0.164632, 0.143156])

	names.append("LWristYaw")
	times.append([0.36, 0.96, 1.44])
	keys.append([0.21932, -0.70875, -0.808459])

	names.append("RElbowRoll")
	times.append([0.44, 1.04, 1.52])
	keys.append([1.01055, 1.08909, 1.30027])

	names.append("RElbowYaw")
	times.append([0.44, 1.04, 1.52])
	keys.append([1.17807, 1.87297, 1.94201])

	names.append("RHand")
	times.append([0.44, 1.04, 1.52])
	keys.append([0.0456001, 0.68, 0.7692])

	names.append("RShoulderPitch")
	times.append([0.44, 1.04, 1.52])
	keys.append([1.29934, 1.5141, 1.2706])

	names.append("RShoulderRoll")
	times.append([0.44, 1.04, 1.52])
	keys.append([-0.176474, -0.115114, -0.116648])

	names.append("RWristYaw")
	times.append([0.44, 1.04, 1.52])
	keys.append([0.0889301, 0.935697, 1.1029])
	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say('I want to help him')
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()
	
	
	
	#FastPointAtUserLeft
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.36, 0.56, 0.72, 1, 1.44, 1.84])
	keys.append([-0.378473, -0.248071, -0.382718, -0.234108, -0.36625, -0.386192])

	names.append("HeadYaw")
	times.append([0.36, 0.72, 1, 1.44, 1.84])
	keys.append([-0.0245859, -0.10282, -0.144238, -0.0951499, -0.0951499])

	names.append("HipPitch")
	times.append([0.48, 1.12, 1.56])
	keys.append([-0.144636, -0.254162, -0.243543])

	names.append("HipRoll")
	times.append([0.48, 1.12, 1.56])
	keys.append([0.00716199, 0.022228, -0.00310838])

	names.append("KneePitch")
	times.append([0.48, 1.12, 1.56])
	keys.append([0.0283312, 0.0946297, 0.0803466])

	names.append("LElbowRoll")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([-1.42811, -0.623083, -0.737812, -1.04154, -1.11211])

	names.append("LElbowYaw")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([-1.18429, -1.19503, -1.25025, -0.971065, -0.929646])

	names.append("LHand")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([0.0984, 0.94, 0.39, 0.09, 0.02])

	names.append("LShoulderPitch")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([1.07222, 0.855211, 0.89428, 1.20261, 1.18881])

	names.append("LShoulderRoll")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([0.486161, 0.460083, 0.461617, 0.45088, 0.429403])

	names.append("LWristYaw")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([-0.918909, -0.90817, -0.918909, -0.101286, 0.145688])

	names.append("RElbowRoll")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([0.874422, 0.898967, 0.926578, 0.733295, 0.70875])

	names.append("RElbowYaw")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([1.38363, 1.27615, 1.5054, 1.59884, 1.53549])

	names.append("RHand")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([0.5008, 0.28, 0.14, 0.1532, 0.1532])

	names.append("RShoulderPitch")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([1.80863, 1.81783, 1.84237, 1.8071, 1.81783])

	names.append("RShoulderRoll")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([-0.119694, -0.275542, -0.295549, -0.176517, -0.16085])

	names.append("RWristYaw")
	times.append([0.4, 0.76, 1.04, 1.48, 1.88])
	keys.append([-0.0767419, -0.0767419, -0.0767419, -0.0767419, -0.0767419])
	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say('And I bet you do too!')
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()
	
	
	
	#LeftArmOnChest
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.3, 1.68])
	keys.append([-0.299375, -0.307887])

	names.append("HeadYaw")
	times.append([0.3, 1.68])
	keys.append([ 0.191709, 0.174472])

	names.append("HipPitch")
	times.append([0.3])
	keys.append([-0.0857175])

	names.append("HipRoll")
	times.append([0.3])
	keys.append([ -0.128879])

	names.append("KneePitch")
	times.append([0.3])
	keys.append([ -0.00222816])

	names.append("LElbowRoll")
	times.append([ 0.3, 1.12, 1.68])
	keys.append([ -0.699764, -2.45762, -1.11033])

	names.append("LElbowYaw")
	times.append([0.3, 1.12, 1.68])
	keys.append([-0.89139, -0.642302, -0.853579])

	names.append("LHand")
	times.append([ 0.3])
	keys.append([ 0.1468])

	names.append("LShoulderPitch")
	times.append([ 0.3, 1.12, 1.68])
	keys.append([1.27883, 0.301266, 1.52426])

	names.append("LShoulderRoll")
	times.append([ 0.3, 1.12, 1.48])
	keys.append([0.415449, 0.0878344, 0.348476])

	names.append("LWristYaw")
	times.append([0.3])
	keys.append([ 0.00149202])

	names.append("RElbowRoll")
	times.append([ 0.3])
	keys.append([ 0.922525])

	names.append("RElbowYaw")
	times.append([0.3])
	keys.append([ 1.67463])

	names.append("RHand")
	times.append([0.3])
	keys.append([ 0.1288])

	names.append("RShoulderPitch")
	times.append([ 0.3])
	keys.append([ 1.92368])

	names.append("RShoulderRoll")
	times.append([0.3])
	keys.append([ -0.357079])

	names.append("RWristYaw")
	times.append([0.3])
	keys.append([ 0.11194])

	
	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say("Let's learn his language")
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()
	
	
	
	#WideOpenBothHands
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.6, 1, 1.4, 1.64])
	keys.append([-0.0802968, -0.195346, -0.281251, -0.302727])

	names.append("HeadYaw")
	times.append([0.6, 1, 1.4, 1.64])
	keys.append([0.022968, 0.05058, 0.030638, 0.05058])

	names.append("HipPitch")
	times.append([0.52, 0.88, 1.12, 1.6])
	keys.append([-0.230881, -0.0257017, -0.0257017, -0.255768])

	names.append("HipRoll")
	times.append([0.52, 0.88, 1.12])
	keys.append([-0.000340311, -0.000340311, -0.000340311])

	names.append("KneePitch")
	times.append([0.52, 0.88, 1.12, 1.6])
	keys.append([0.0723167, -0.00966694, -0.00966694, 0.114746])

	names.append("LElbowRoll")
	times.append([0.56, 1, 1.4, 1.68])
	keys.append([-0.651908, -0.361981, -0.389594, -0.363515])

	names.append("LElbowYaw")
	times.append([0.56, 1, 1.4, 1.68])
	keys.append([-1.28848, -1.60142, -1.6459, -1.60142])

	names.append("LHand")
	times.append([0.56, 1, 1.4, 1.68])
	keys.append([0.3068, 0.82, 0.68, 0.1])

	names.append("LShoulderPitch")
	times.append([0.56, 1, 1.4, 1.68])
	keys.append([1.42351, 1.4097, 1.3913, 1.4097])

	names.append("LShoulderRoll")
	times.append([0.56, 1, 1.4, 1.68])
	keys.append([0.322343, 0.446958, 0.21803, 0.144399])

	names.append("LWristYaw")
	times.append([0.56, 1, 1.4, 1.68])
	keys.append([-0.415757, -1.06464, -0.584497, -0.475581])

	names.append("RElbowRoll")
	times.append([0.64, 0.96, 1.36, 1.68])
	keys.append([0.604439, 0.57836, 0.538476, 0.509331])

	names.append("RElbowYaw")
	times.append([0.64, 0.96, 1.36, 1.68])
	keys.append([1.1394, 1.74226, 1.64715, 1.60573])

	names.append("RHand")
	times.append([0.64, 0.96, 1.36, 1.68])
	keys.append([0.3068, 0.82, 0.68, 0.1])

	names.append("RShoulderPitch")
	times.append([0.64, 0.96, 1.36, 1.68])
	keys.append([1.41132, 1.38524, 1.43587, 1.47115])

	names.append("RShoulderRoll")
	times.append([0.64, 0.96, 1.36, 1.68])
	keys.append([-0.414847, -0.566031, -0.384166, -0.295195])

	names.append("RWristYaw")
	times.append([0.64, 0.96, 1.36, 1.68])
	keys.append([0.389594, 0.803775, 0.312894, 0.199378])
	
	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
	def speech():
		self.say('And make him happy!')
		
	motion_thread = threading.Thread(target=motion)
	speech_thread = threading.Thread(target=speech)
	motion_thread.start()
	speech_thread.start()
	motion_thread.join()
	speech_thread.join()
	

	self.normalPosture()
	
    def strong(self):

        names = list()
        times = list()
        keys = list()

        names.append("HeadPitch")
        times.append([0.35, 0.75, 0.91])
        keys.append([0.0907571, 0.10472, 0.410152])

        names.append("HeadYaw")
        times.append([0.75, 0.91])
        keys.append([0.242601, 0.21293])

        names.append("HipPitch")
        times.append([0.35])
        keys.append([0.0994838])

        names.append("HipRoll")
        times.append([0.35, 0.75])
        keys.append([-0.0925025, -0.150098])

        names.append("LElbowRoll")
        times.append([0.35, 0.75, 0.91])
        keys.append([-0.645772, -1.04545, -1.56207])

        names.append("LElbowYaw")
        times.append([0.75, 0.91])
        keys.append([-1.04545, -1.40674])

        names.append("LHand")
        times.append([0.35, 0.75, 0.91])
        keys.append([0.35, 0.28, 0.02])

        names.append("LShoulderPitch")
        times.append([0.35, 0.75, 0.91])
        keys.append([-0.989602, -0.537561, 0.0628319])

        names.append("LShoulderRoll")
        times.append([0.35, 0.75, 0.91])
        keys.append([0.322886, 0.340339, 0.216421])

        names.append("LWristYaw")
        times.append([0.35, 0.75, 0.91])
        keys.append([-0.420624, -1.61617, -1.71566])

        names.append("RElbowRoll")
        times.append([0.35, 0.75])
        keys.append([1.02451, 1.56207])

        names.append("RElbowYaw")
        times.append([0.35, 0.75])
        keys.append([0.471239, -0.0855211])

        names.append("RHand")
        times.append([0.35, 0.75])
        keys.append([0.54, 0.98])

        names.append("RShoulderPitch")
        times.append([0.35, 0.75])
        keys.append([1.01753, 0.904081])

        names.append("RShoulderRoll")
        times.append([0.35, 0.75])
        keys.append([-0.568977, -0.748746])

        names.append("RWristYaw")
        times.append([0.35, 0.75])
        keys.append([-0.0244346, 0.403171])

        def motion():
		    self.motion_service.angleInterpolation(names, keys, times, True)
        def speech():
		    self.say('Good job')
		
        motion_thread = threading.Thread(target=motion)
        speech_thread = threading.Thread(target=speech)
        motion_thread.start()
        time.sleep(0.8)
        speech_thread.start()
        motion_thread.join()
        speech_thread.join()

        time.sleep(0.5)
        self.normalPosture()

    def highfive(self):

        names = list()
        times = list()
        keys = list()

        names.append("HeadPitch")
        times.append([0.76])
        keys.append([-0.148608])

        names.append("HeadYaw")
        times.append([0.76])
        keys.append([-0.326248])

        names.append("HipPitch")
        times.append([0.76])
        keys.append([-0.0305311])

        names.append("HipRoll")
        times.append([0.76])
        keys.append([0.130031])

        names.append("KneePitch")
        times.append([0.76])
        keys.append([-0.0164125])

        names.append("LElbowRoll")
        times.append([0.76])
        keys.append([-1.3706])

        names.append("LElbowYaw")
        times.append([0.76])
        keys.append([-0.241797])

        names.append("LHand")
        times.append([0.76])
        keys.append([0.96824])

        names.append("LShoulderPitch")
        times.append([0.76])
        keys.append([1.15775])

        names.append("LShoulderRoll")
        times.append([0.76])
        keys.append([0.676271])

        names.append("LWristYaw")
        times.append([0.76])
        keys.append([0.406393])

        names.append("RElbowRoll")
        times.append([0.76])
        keys.append([1.13603])

        names.append("RElbowYaw")
        times.append([0.76])
        keys.append([1.37554])

        names.append("RHand")
        times.append([0.76])
        keys.append([0.957623])

        names.append("RShoulderPitch")
        times.append([0.76])
        keys.append([-0.155174])

        names.append("RShoulderRoll")
        times.append([0.76])
        keys.append([-0.147616])

        names.append("RWristYaw")
        times.append([0.76])
        keys.append([-1.20283])

        def motion():
		    self.motion_service.angleInterpolation(names, keys, times, True)
        def speech():
		    self.say("High five!!")

        motion_thread = threading.Thread(target=motion)
        speech_thread = threading.Thread(target=speech)
        motion_thread.start()
        time.sleep(0.8)
        speech_thread.start()
        motion_thread.join()
        speech_thread.join()

        time.sleep(0.5)
        self.normalPosture()

        #magari qua invece del timer mettiamo che riconosce il tocco e quindi toglie la mano,
        #alternativamente rimane li per un tot... tra i sensori in questo file c'e'
        #elif (sensorname == 'righthandtouch'): return self.handTouch[1], mi sa 
        #che va scritto in demo?

    def comehere(self):

	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([0.64, 0.72, 0.92, 1])
	keys.append([-0.0610865, 0.111701, -0.172788, 0.0506145])

	names.append("HipPitch")
	times.append([0.64, 0.92])
	keys.append([0.109956, 0.109956])

	names.append("LElbowRoll")
	times.append([0.64, 0.92])
	keys.append([-1.56207, -1.56207])

	names.append("LElbowYaw")
	times.append([0.64, 0.92])
	keys.append([-1.39801, -1.39801])

	names.append("LHand")
	times.append([0.64, 0.72, 0.92, 1])
	keys.append([0.98, 0.38, 0.98, 0.38])

	names.append("LShoulderPitch")
	times.append([0.64, 0.92])
	keys.append([0.563741, 0.563741])

	names.append("LWristYaw")
	times.append([0.64, 0.92])
	keys.append([-1.33169, -1.33169])

	names.append("RElbowRoll")
	times.append([0.64, 0.92])
	keys.append([1.56207, 1.56207])

	names.append("RElbowYaw")
	times.append([0.64, 0.92])
	keys.append([0.411898, 0.411898])

	names.append("RShoulderPitch")
	times.append([0.64, 0.92])
	keys.append([1.57603, 1.57603])

	names.append("RShoulderRoll")
	times.append([0.64, 0.92])
	keys.append([-0.516617, -0.516617])

	
	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
        def speech():
		self.say("Come here!")

        motion_thread = threading.Thread(target=motion)
        speech_thread = threading.Thread(target=speech)
        motion_thread.start()
        time.sleep(0.8)
        speech_thread.start()
        motion_thread.join()
        speech_thread.join()

        time.sleep(0.5)
        self.normalPosture()



    def sad(self):
	  
	  isAbsolute = True
	  # defeat posture
	  jointNames = ["RElbowRoll", "RElbowYaw", "RShoulderPitch", "RShoulderRoll", "LElbowRoll", "LElbowYaw", "LShoulderPitch", "LShoulderRoll", "HeadPitch", "HipPitch"]

	  jointValues = [1.38, 0.382, 1.33, -0.69, -1.42, -0.333, 1.24, 0.699, 0.445, -0.52]
	  times = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
	  self.motion_service.angleInterpolation(jointNames, jointValues, times, isAbsolute)
	  [22.0, -22.0]

	  # pepper shakes his head
	  # gradi = 22.0 --> rad = 0.38
	  self.motion_service.angleInterpolation("HeadYaw", 0.30, 0.4, isAbsolute)
	  
	  # gradi = -22.0 --> rad = -0.38
	  self.motion_service.angleInterpolation("HeadYaw", -0.30, 0.4, isAbsolute)

	  # gradi = 22.0 --> rad = 0.38
	  self.motion_service.angleInterpolation("HeadYaw", 0.30, 0.4, isAbsolute)
	  
	  self.normalPosture()
	  return
	  
	  
    def sad2(self):

	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0.42586, 0.42586, 0.42586, 0.42586, 0.42586])

	names.append("HeadYaw")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0.113446, 0.429351, 0.113446, -0.204204, 0.113446])

	names.append("HipPitch")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([-0.457276, -0.457276, -0.457276, -0.457276, -0.457276])

	names.append("HipRoll")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0, 0, 0, 0, 0])

	names.append("KneePitch")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([-0.0174533, -0.0174533, -0.0174533, -0.0174533, -0.0174533])

	names.append("LElbowRoll")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([-0.363028, -0.363028, -0.363028, -0.363028, -0.363028])

	names.append("LElbowYaw")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([-0.884882, -0.884882, -0.884882, -0.884882, -0.884882])

	names.append("LHand")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0.31, 0.31, 0.31, 0.31, 0.31])

	names.append("LShoulderPitch")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([1.29503, 1.29503, 1.29503, 1.29503, 1.29503])

	names.append("LShoulderRoll")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0.0191986, 0.139626, 0.0191986, 0.139626, 0.0191986])

	names.append("RElbowRoll")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0.546288, 0.546288, 0.546288, 0.546288, 0.546288])

	names.append("RElbowYaw")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0.933751, 0.933751, 0.933751, 0.933751, 0.933751])

	names.append("RHand")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([0.33, 0.33, 0.33, 0.33, 0.33])

	names.append("RShoulderPitch")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([1.32296, 1.32296, 1.32296, 1.32296, 1.32296])

	names.append("RShoulderRoll")
	times.append([1.16, 1.96, 2.76, 3.56, 4.36])
	keys.append([-0.0418879, -0.176278, -0.0418879, -0.176278, -0.0418879])

	def motion():
		self.motion_service.angleInterpolation(names, keys, times, True)
        def speech():
		self.say("Why don't you want to play with me?")

        motion_thread = threading.Thread(target=motion)
        speech_thread = threading.Thread(target=speech)
        motion_thread.start()
        time.sleep(1.3)
        speech_thread.start()
        motion_thread.join()
        speech_thread.join()

        time.sleep(0.5)
        self.normalPosture()

	
    def pepperVictory(self):
    # animazione del robot quando vince il gioco

        isAbsolute = True

        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
        jointValues = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07, -0.141, 0.46, -0.892, 0.8, 0.98]
        times  = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.motion_service.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        
        for i in range(2):
            jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
            jointValues = [2.7, -1.3, -0.07, -0.07]
            times  = [0.6, 0.6, 0.6, 0.6]
            self.motion_service.angleInterpolation(jointNames, jointValues, times, isAbsolute)

            jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
            jointValues = [1.3, -2.7, -0.07, -0.07]
            times  = [0.6, 0.6, 0.6, 0.6]
            self.motion_service.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        
        self.normalPosture()
        return
	
	


    

    def moveHorizontalRight(robot):
	 # animazione del robot quando muove la macchina in orizzontale verso destra
	 session = robot.session_service("ALMotion")
	 isAbsolute = True

	 # move posture
	 jointNames = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
	 jointValues = [1.30, 1.28,  0.92, 1.20, -0.92, -0.60]
	 times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
	 session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
	  
	 # robot hand grasps cars
	 session.angleInterpolation("RHand", 0.52, 0.3, isAbsolute)
	  
	  # arm that slides to move the car
	 jointNames = ["RElbowRoll", "RElbowYaw", "RShoulderRoll", "RWristYaw"]
	 jointValues = [1.38, 1.23, -0.25, -1.22]
	 times = [0.6, 0.6, 0.6, 0.6]
	 session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

	 robot.normalPosture()
	 return

    # Head motion

    def headPose(self, yaw, pitch, tm):
        jointNames = ["HeadYaw", "HeadPitch"]
        initAngles = [yaw, pitch]
        timeLists  = [tm, tm]
        isAbsolute = True
        self.motion_service.angleInterpolation(jointNames, initAngles, timeLists, isAbsolute)


    def headscan(self):
        jointNames = ["HeadYaw", "HeadPitch"]
        # look left
        initAngles = [1.6, -0.2]
        timeLists  = [5.0, 5.0]
        isAbsolute = True
        self.motion_service.angleInterpolation(jointNames, initAngles, timeLists, isAbsolute)
        # look right
        finalAngles = [-1.6, -0.2]
        timeLists  = [10.0, 10.0]
        self.motion_service.angleInterpolation(jointNames, finalAngles, timeLists, isAbsolute)
        # look ahead center
        finalAngles = [0.0, -0.2]
        timeLists  = [5.0, 5.0]
        self.motion_service.angleInterpolation(jointNames, finalAngles, timeLists, isAbsolute)
        

    # Arms stiffness [0,1]
    def setArmsStiffness(self, stiff_arms):
        names = "LArm"
        stiffnessLists = stiff_arms
        timeLists = 1.0
        self.motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)
        names = "RArm"
        self.motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)


    # Wait

    def wait(self, r=1):
        print 'wait',r
        for i in range(0,r):
            time.sleep(3)

    # Sensors

    def sensorvalue(self, sensorname='all'):
        if (sensorname == 'frontsonar'):
            return self.sonar[0]
        elif (sensorname == 'rearsonar'):
            return self.sonar[1]
        elif (sensorname == 'headtouch'):
            return self.headTouch
        elif (sensorname == 'lefthandtouch'):
            return self.handTouch[0]
        elif (sensorname == 'righthandtouch'):
            return self.handTouch[1]
        elif (sensorname == 'frontlaser'):
            return self.frontlaser
        elif (sensorname == 'all'):
            return [self.frontlaser,  self.sonar[0],  self.sonar[1],
                self.headTouch, self.handTouch[0], self.handTouch[1] ]


    def sensorvaluestring(self):
        return '%.1f,%.1f,%.1f,%d,%d,%d' %(self.sensorvalue('frontlaser'),self.sensorvalue('frontsonar'),self.sensorvalue('rearsonar'),self.sensorvalue('headtouch'),self.sensorvalue('lefthandtouch'),self.sensorvalue('righthandtouch'))



    # Behaviors

    def normalPosture(self):
        jointValues = [0.00, -0.21, 1.55, 0.13, -1.24, -0.52, 0.01, 1.56, -0.14, 1.22, 0.52, -0.01,
                       0, 0, 0, 0, 0]
        isAbsolute = True
        self.motion_service.angleInterpolation(self.jointNames, jointValues, 3.0, isAbsolute)


    def setPosture(self, jointValues):
        isAbsolute = True
        self.motion_service.angleInterpolation(self.jointNames, jointValues, 3.0, isAbsolute)

    def getPosture(self):
        pose = None
        useSensors = True
        pose = self.motion_service.getAngles(self.jointNames, useSensors)
        return pose



    def raiseArm(self, which='R'): # or 'R'/'L' for right/left arm
        if (which=='R'):
            jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
            jointValues = [ -1.0, -0.3, 1.22, 0.52, -1.08]
        else:
            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
            jointValues = [ -1.0, 0.3, -1.22, -0.52, 1.08]

        isAbsolute = True
        self.motion_service.angleInterpolation(jointNames, jointValues, 3.0, isAbsolute)


    def stand(self):
        if self.al_service.getState()!='disabled':
            self.al_service.setState('disabled')
        self.rp_service.goToPosture("Stand",2.0)

    def disabled(self):
        #self.tts_service.say("Bye bye")
        self.al_service.setState('disabled')

    def interactive(self):
        #tts_service.say("Interactive")
        self.al_service.setState('interactive')


    def run_behavior(self, bname):
        if self.beh_service!=None:
            try:
                self.beh_service.startBehavior(bname)
                #time.sleep(10)
                #self.beh_service.stopBehavior(bname)
            except:
                pass

    def sax(self):
        str = 'sax'
        print(str)
        bname = 'saxophone-0635af/behavior_1'
        self.run_behavior(bname)

    def dance(self):
        str = 'dance'
        print(str)
        bname = 'dance/behavior_1'
        self.run_behavior(bname)

    def takephoto(self):
        str = 'take photo'
        print(str)
        #tts_service.say("Cheers")
        bname = 'takepicture-61492b/behavior_1'
        self.run_behavior(bname)

    def introduction(self):
        str = 'introduction'
        print(str)
        bname = 'animated-say-5b866d/behavior_1'
        self.run_behavior(bname)


    def explain(self):
        str = 'Explaining...'
        print(str)
        bname = '.lastUploadedChoregrapheBehavior/animations/Explain/behavior.xar'
        self.run_behavior(bname)

    # People

    def getPeopleInfo(self):
        pl = self.memory_service.getData('PeoplePerception/PeopleList')
            # PeoplePerception/PeopleList
        print('People list: %s' %str(pl))
        r = []
        for id in pl:
            print('Person ID %d' %id)
            gekey = 'PeoplePerception/Person/%d/GenderProperties' %id
            smkey = 'PeoplePerception/Person/%d/SmileProperties' %id
            agkey = 'PeoplePerception/Person/%d/AgeProperties' %id

            ge = self.memory_service.getData(gekey)  # 0 female, 1 male, confidence
            sm = self.memory_service.getData(smkey)  # 0-1 smile, confidence
            ag = self.memory_service.getData(agkey)  # age, confidence
            d = {}
            d['gender'] = ge
            d['age'] = ag
            d['smile'] = sm
            r.append(d) 
            #rstr= "gender: %s, age: %s, smile: %s" %(str(ge),str(ag),str(sm))
            #print(rtrs)
        return r

    # Battery

    def getBatteryCharge(self):
        return self.battery_service.getBatteryCharge()


    # Memory

    def memset(self, key, val):
        self.memory_service.insertData(key,val)

    def memget(self, key):
        try:
            return self.memory_service.getData(key)
        except:
            return ''

    # Logging functions

    def logenable(self,enable=True):
        if enable:
            if (self.logfile is None):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                logfilename = '/tmp/pepper_%s.log' %timestamp
                self.logfile = open(logfilename,'a')
                self.lthr = threading.Thread(target = self.logthread)
                self.lthr.start()
                print('Log enabled on file %s.' %logfilename)
        else:
            if (self.logfile is not None):
                self.logclose()
                self.lthr.do_run = False
                self.lthr = None
                print('Log disabled.')


    def logdata(self, data):
        if (self.logfile is not None):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.logfile.write("%s;%r\n" %(timestamp, data))
            self.logfile.flush()

    def logclose(self):
        if (self.logfile != None):
            self.logfile.close()
            self.logfile = None


    def logthread(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            try:
                z = self.getState()
                self.logdata(z)
            except:
                pass
            time.sleep(1)


    def setFERserver(self,ip,port=5678):
        self.FER_server_IP = ip
        self.FER_server_port = port


    def getState(self):
        # v1
        # frontlaser, frontsonar, backsonar, headtouch, lefthandtouch, 
        # righthandtouch, screenx, screeny, face, happy
        # v2
        # frontlaser, frontsonar, backsonar, headtouch, lefthandtouch, 
        # righthandtouch, head_yaw, head_pitch, screenx, screeny, touchcnt, face, happy
        
        z = self.sensorvalue() # frontlaser...handtouch
        useSensors = True
        headPose = self.motion_service.getAngles(["HeadYaw", "HeadPitch"],
                                                 useSensors)
        z.append(headPose[0])
        z.append(headPose[1])
        z.append(self.screenTouch[0])
        z.append(self.screenTouch[1])
        z.append(touchcnt)
        z.append(1.0 if self.got_face else 0.0)
        if self.FER_server_IP is not None:
            r = self.sendImage(self.FER_server_IP,self.FER_server_port)
        else:
            r = None
        v = []
        if r is not None and type(r)!=type('str'):
            v = eval(r)
        h = 0.0
        for c in v:
            h = max(h,c[1])
        z.append(h)    
        return z

