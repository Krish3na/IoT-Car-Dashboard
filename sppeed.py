
import RPi.GPIO as GPIO
import time
import math

sensor=17
M1=23
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(M1,GPIO.OUT)

sample=1000
count=0
D=0.025
Last=0
start=0
speed=0
end=0


def set_start():
    global start
    start = time.time()

def set_end():
    global end
    end = time.time()

def get_rpm():
    global count, D, speed
    if not count:
        set_start()
        count+=1
    else:
        count+=1

    if  count==sample:
        set_end()
        delta=end-start
        delta=delta/60
        rpm=(sample/delta)/2
        print("RPM is "+ str(rpm))
        speed=(rpm* math.pi* D)/60
        print("Speed is "+str(speed)+" m/s")
        count=0

def speed_measure():
    global Last
    GPIO.output(M1,1)
    try:
        while True:
            
            In=GPIO.input(sensor)
            if GPIO.input(sensor)==0 and Last==1:
                get_rpm()
            Last=In
            
    except KeyboardInterrupt:
        GPIO.output(M1,0)
        print("Quit")
        GPIO.cleanup()

if __name__=="__main__":
    #GPIO.add_event_detect(sensor, GPIO.RISING, callback=get_rpm)
    #time.sleep(0.1)
    speed_measure()
    
