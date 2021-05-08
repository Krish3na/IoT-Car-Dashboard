import thingspeak
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import concurrent.futures
import threading
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
from finalclasscode import PhotoBoothApp


GPIO.setwarnings(False)
threads = []

#----------thingspeak
channel_id = 1369326 # PUT CHANNEL ID HERE
write_key  = 'KICCPBO0LQ99HUJ5' # PUT YOUR WRITE KEY HERE
read_key   = 'K0CRWSZFNVHVBESY' # PUT YOUR READ KEY HERE
#----------dht
dht_pin = 4
sensor_dht = Adafruit_DHT.DHT22
#----------speed measure
sensor=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN,GPIO.PUD_UP)

sample = 1000# how many half revolutions to time
count,start,end= 0,0,0
speed=0
D=2.5
Last=0
temp1=1
#------------gps
gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
h,t=0,0

def measure_dht(channel):
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor_dht, dht_pin)
        
        if humidity:
            # write
            h,t=humidity, temperature
            response = channel.update({'field1': temperature, 'field2': humidity})
            print("\nDHTT")
            print ('Humidity :'+str(humidity)+' Temperature :'+str(temperature)+'\n')
            time.sleep(6)
        else:
            response = channel.update({'field1': t, 'field2': h})
            print("\nDHTT")
            print ('Humidity :'+str(h)+' Temperature :'+str(t)+'\n')
            time.sleep(6)
            

            
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

def gps(channel):
        while True:
                received_data = (str)(ser.readline())                   #read NMEA string received
                GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
                if (GPGGA_data_available>0):
                    GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                    NMEA_buff = (GPGGA_buffer.split(','))             #store comma separated data in buffer
                    #print(NMEA_buff)
                    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
                    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
                    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
                    
                    #print("NMEA Time: ", nmea_time,'\n')
                    #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
                    
                    lat = float(nmea_latitude)                  #convert string into float for calculation
                    longi = float(nmea_longitude)               #convertr string into float for calculation
                    
                    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
                    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format                                         #get time, latitude, longit
                    
                    response = channel.update({'field3': lat_in_degrees, 'field4': long_in_degrees})
                    print("\nGPS")
                    print("lat in degrees:"+str(lat_in_degrees)+" long in degree: "+str(long_in_degrees))
                    map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map
                    print(str(map_link)+'\n')
                    sleep(4)

                else:
                    response = channel.update({'field3': lat_in_degrees, 'field4': long_in_degrees})
                    print("\nGPS")
                    print("lat in degrees:"+str(lat_in_degrees)+" long in degree: "+str(long_in_degrees))
                    map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map
                    print(str(map_link)+'\n')
                    sleep(4)

def set_start():
    global start
    start = time.time()

def set_end():
    global end
    end = time.time()

def get_rpm(channel):
    global count, D, speed,speed1
    
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
        speed=(rpm*0.001885* D)
        speed1=speed
        response = channel.update({'field5': speed})
        print("\nSpeed Measuring")
        print("RPM is "+ str(rpm)+" rpm")
        print("Speed is "+str(speed)+" kmph\n")
        count=0

def speed_measure(channel):
    global Last
    #GPIO.output(in1,1)
    while True:
            
            In=GPIO.input(sensor)
            if GPIO.input(sensor)==0 and Last==1:
                get_rpm(channel)
                
            Last=In




def car():
    pba = PhotoBoothApp()
    pba.root.mainloop()
        


if __name__=="__main__":
        try:
            channel = thingspeak.Channel(id=channel_id,api_key=write_key)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                f1 = executor.submit(measure_dht,channel)
                f2 = executor.submit(speed_measure,channel)
                f3 = executor.submit(gps,channel)
                f4 = executor.submit(car)

            print(f1.result())
            print(f2.result())
            print(f3.result())
            print(f4.result())
            
        except KeyboardInterrupt:
            GPIO.output(in1,0)
            print("Quit")
            webbrowser.open(map_link)
            GPIO.cleanup()
    
        '''
        t1 = threading.Thread(target=measure_dht, args=[channel])
        t2 = threading.Thread(target=speed_measure)
        t3 = threading.Thread(target=gps)
        t1.start()
        threads.append(t1)
        t2.start()
        threads.append(t2)
        t3.start()
        threads.append(t3)

        for thread in threads:
            thread.join()
        '''  

