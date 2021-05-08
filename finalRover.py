from __future__ import print_function
import tkinter as tki
import threading
import datetime
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
in1,in2=23,24
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setwarnings(False)

class PhotoBoothApp:
        def __init__(self):
   
                self.thread = None
                #self.stopEvent = None
                # initialize the root window and image panel
                self.root = tki.Tk()
                #self.panel = None

    
                btn = tki.Button(self.root, text="forward", command=self.forward)
                btn.pack(side="top", fill="x", expand="yes", padx=10,pady=10)
                #b2 = tki.Button(self.root, text="On Sensors", command=self.takeSnapshot)
                #b2.pack(side="bottom", fill="x", expand="no", padx=10,pady=10)
                b1 = tki.Button(self.root, text="backward", command=self.backward)
                b1.pack(side="bottom", fill="x", expand="no", padx=10,pady=10)
                b3 = tki.Button(self.root, text="right", command=self.right)
                b3.pack(side="right", fill="y", expand="no", padx=5,pady=5)
                b4 = tki.Button(self.root, text="left", command=self.left)
                b4.pack(side="left", fill="y", expand="no", padx=5,pady=5)
                b5 = tki.Button(self.root, text="stop", command=self.stop)
                b5.pack(side="bottom", fill="y", expand="no", padx=10,pady=10)

                self.root.wm_title("Car Control")
                self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
                
        def forward(self):
                print("Forward")
                GPIO.output(7,False)
                GPIO.output(11,True)
                GPIO.output(13,False)
                GPIO.output(15,True)
                GPIO.output(23,False)
                GPIO.output(24,True)
        def backward(self):
                GPIO.output(7,True)
                GPIO.output(11,False)
                GPIO.output(13,True)
                GPIO.output(15,False)
                GPIO.output(23,True)
                GPIO.output(24,False)
                print("Backward")
        def right(self):
                GPIO.output(7,True)
                GPIO.output(11,False)
                GPIO.output(13,False)
                GPIO.output(15,True)
                GPIO.output(23,False)
                GPIO.output(24,True)
                print("Right")
        def left(self):
                GPIO.output(7,False)
                GPIO.output(11,True)
                GPIO.output(13,True)
                GPIO.output(15,False)
                GPIO.output(23,False)
                GPIO.output(24,True)
                print("Left")
        def stop(self):
                GPIO.output(7,False)
                GPIO.output(11,False)
                GPIO.output(13,False)
                GPIO.output(15,False)
                GPIO.output(23,False)
                GPIO.output(24,False)
                print("stop")
     
        #def takeSnapshot(self):
                #print("Working on Sensors....")
                #main()

        def onClose(self):

                print("[INFO] closing...")
                #self.stopEvent.set()
                #self.vs.stop()
                self.root.quit()

