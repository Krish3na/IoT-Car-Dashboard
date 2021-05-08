import multiprocessing as m
import thingspeak
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
#----------thingspeak
channel_id = 1369326 # PUT CHANNEL ID HERE
write_key  = 'KICCPBO0LQ99HUJ5' # PUT YOUR WRITE KEY HERE
read_key   = 'K0CRWSZFNVHVBESY' # PUT YOUR READ KEY HERE
#----------dht
dht_pin = 4
sensor = Adafruit_DHT.DHT22
#----------speed measure
speed_pin = 21 # define the GPIO pin our sensor is attached to
GPIO.setmode(GPIO.BCM) # set GPIO numbering system to BCM
GPIO.setup(speed_pin,GPIO.IN) # set our sensor pin to an input
sample = 1000# how many half revolutions to time
count,start,end= 0,0,0
 
def measure_dht(channel):
    try:
        while True:
            print("DHTT")
            '''
            humidity, temperature = Adafruit_DHT.read_retry(sensor, dht_pin)
            # write
            response = channel.update({'field1': temperature, 'field2': humidity})
            print('Humidity :',humidity,'Temperature :', temperature)
            # free account has an api limit of 15sec
            time.sleep(15)
            # read
            #read = channel.get({})
            #print("Read:", read)
            '''

    except KeyboardInterrupt:
            print("Quit")
 	    #GPIO.cleanup()

def set_start():
    global start
    start = time.time()

def set_end():
    global end
    end = time.time()

def get_rpm(c):
    global count
    if not count:
        set_start()
        count+=1

    else:
        count+=1

    if count==sample:
        set_end()
        delta=end-start
        delta=delta/60
        rpm=(sample/delta)/2
        print(rpm)
        count=0
 	
def speed_measure():
    print("speed measuring")
    '''
    GPIO.add_event_detect(speed_pin, GPIO.RISING, callback=get_rpm)
    # execute the get_rpm function when a HIGH signal is detected
    '''
    try:
        while True: # create an infinte loop to keep the script running
            #get_rpm()
            time.sleep(0.1)
    except KeyboardInterrupt:
            print ("Quit")
            #GPIO.cleanup()
    
'''    
def run_parallel(*functions):

    #Run functions in parallel

    from multiprocessing import Process
    processes = []
    for function in functions:
        proc = Process(target=function)
        proc.start()
        processes.append(proc)
    for proc in processes:
        proc.join()
'''
    
processes = []


if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id,api_key=write_key)
    p1=m.Process(target=speed_measure)
    p2=m.Process(target=measure_dht,args=[channel])
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    #processes.append(p1)
    #processes.append(p2)

#for p in processes:
    #p.join()
    

#finish=time.perf_counter()
#print("fininshing",finish)
        
        
