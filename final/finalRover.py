from __future__ import print_function
import tkinter as tki
import threading
import datetime
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
in1,in2=27,22
in3,in4=19,26
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
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
                b2 = tki.Button(self.root, text="Movement", command=self.dance)
                b2.pack(side="bottom", fill="x", expand="no", padx=10,pady=10)
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
                GPIO.output(in3,False)
                GPIO.output(in4,True)
                GPIO.output(in1,False)
                GPIO.output(in2,True)

        def backward(self):
                GPIO.output(in3,True)
                GPIO.output(in4,False)
                GPIO.output(in1,True)
                GPIO.output(in2,False)
                print("Backward")
                
        def right(self):
                GPIO.output(in3,True)
                GPIO.output(in4,False)
                GPIO.output(in1,False)
                GPIO.output(in2,True)
                print("Right")
                
        def left(self):
                GPIO.output(in3,False)
                GPIO.output(in4,True)
                GPIO.output(in1,True)
                GPIO.output(in2,False)
                print("Left")
                
        def stop(self):
                GPIO.output(in3,False)
                GPIO.output(in4,False)
                GPIO.output(in1,False)
                GPIO.output(in2,False)
                print("stop")
     
        def dance(self):
                print("dance")
                GPIO.output(in4,True)
                GPIO.output(in2,True)
                time.sleep(1)
                GPIO.output(in3,True)
                GPIO.output(in4,False)
                GPIO.output(in1,True)
                GPIO.output(in2,False)
                time.sleep(1)
                GPIO.output(in3,True)
                GPIO.output(in4,False)
                GPIO.output(in1,False)
                GPIO.output(in2,True)
                time.sleep(1)
                GPIO.output(in3,False)
                GPIO.output(in4,True)
                GPIO.output(in1,True)
                GPIO.output(in2,False)
                time.sleep(1)
                GPIO.output(in4,False)
                GPIO.output(in1,False)

        def onClose(self):

                print("[INFO] closing...")
                #self.stopEvent.set()
                #self.vs.stop()
                self.root.quit()

