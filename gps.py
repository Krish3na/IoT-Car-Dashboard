'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
import threading

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

threads = []
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

def gps():
        try:
            while True:
                received_data = (str)(ser.readline())
                print(received_data)
                #read NMEA string received
                GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
                if (GPGGA_data_available>0):
                    GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                    NMEA_buff = (GPGGA_buffer.split(','))             #store comma separated data in buffer
                    print(NMEA_buff)
                    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
                    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
                    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
                    
                    #print("NMEA Time: ", nmea_time,'\n')
                    #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
                    
                    lat = float(nmea_latitude)                  #convert string into float for calculation
                    longi = float(nmea_longitude)               #convertr string into float for calculation
                    
                    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
                    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format                                         #get time, latitude, longitude
         
                    print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
                    map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
                    print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
                    print("------------------------------------------------------------\n")
                    sleep(4)
                                
        except KeyboardInterrupt:
            webbrowser.open(map_link)        #open current position information in google map
    



if __name__ =="__main__":

    t3 = threading.Thread(target=gps)
    t3.start()
    threads.append(t3)

    for thread in threads:
        thread.join()
    


    sys.exit(0)
