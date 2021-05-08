#!/usr/bin/python

import RPi.GPIO as GPIO
import time

sensor = 17 # define the GPIO pin our sensor is attached to
M1 = 23
GPIO.setmode(GPIO.BCM) # set GPIO numbering system to BCM
#GPIO.setup(sensor,GPIO.IN) # set our sensor pin to an input
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(M1, GPIO.OUT)
sample = 1000# how many half revolutions to time
count = 0
Last=0
start = 0
end = 0

def set_start():
 	global start
 	start = time.time()

def set_end():
 	global end
 	end = time.time()

def get_rpm(c):
 	global count # delcear the count variable global so we can edit it

 	if not count:
                set_start()
 	 	count+=1
 	else:
                count+=1

 	if count==sample:
 	 	set_end() # create end time
 	 	delta = end - start # time taken to do a half rotation in seconds
 	 	delta = delta / 60 # converted to minutes
 	 	rpm = (sample / delta) / 2 # converted to time for a full single rotation
 	 	print (rpm)
 	 	count = 0 # reset the count to 0

#GPIO.add_event_detect(sensor, GPIO.RISING, callback=get_rpm) # execute the get_rpm function when a HIGH signal is detected
GPIO.output(M1, 1)
try:
        while True: # create an infinte loop to keep the script running
                In = GPIO.input(Encode)
                if GPIO.input(Encode) == 0 and Last == 1:
                        get_rpm()
                Last=In
except KeyboardInterrupt:
        print ("Quit")
 	GPIO.cleanup()
 
