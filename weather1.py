#Importing Packages required to run a Program
import time
import urllib3 #This module is for Thingspeak(URL Handling Module)
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD # This module is for LCD(16X2)
#from Adafruit_BMP085 import BMP085 # This module is for Pressure Sensor(BMP180)80
import Adafruit_DHT # This module is for Humidity Sensor(DHT11)
#BOTH the sensors can measure Temperature
GPIO.setwarnings(False)
key="HKXM1QEC4PTZDXXY" # Type your Write API key from ThingSpeak
lcd=CharLCD(pin_rs=12,pin_e=16,pins_data=[18,36,38,40],numbering_mode=GPIO.BOARD) # Initialisation of LCD PINS
#bmp= BMP085(0x77) # Initialisation of BMP085(Port)
DHT,Pin = [11,4] # Initialisation of DHT11 pins (here 4 is GPIO4)
#The following lines will be displayed on LCD with certain delays
lcd.write_string("ECIL")
lcd.write_string("\n\rWelcomes you")
time.sleep(3)
lcd.clear() # Clears the text on LCD
lcd.write_string("RPI Weather \n\rMonitoring")
time.sleep(2)
#This is the Main function executes continuously
def main():
    print ('System Ready...')
    URL = 'https://api.thingspeak.com/update?api_key=%s' % key
    print ("Wait....")
    while True:
        humi,temp= Adafruit_DHT.read_retry(DHT,Pin)
        #temp=bmp.readTemperature()
        #pressure=bmp.readPressure()/100.0
        #altitude=bmp.readAltitude()
        lcd.clear()
        lcd.write_string("Humi#Temp#P(hPa)")
        lcd.write_string("\n\r%s" %humi+" %sC" %temp)
        finalURL = URL+"&field1=%s&field2=%s" %(humi, temp) # URL which is used to upload the values to website
        http = urllib3.PoolManager()
        response = http.request('GET', finalURL)

        #s= urllib2.urlopen(finalURL); # This command opens the URL for fetching data
        #http.close() # Closing the URL
        print("Humidity : "+str(humi)+"\nTemperature : {0} C".format(temp))
        print("----------------------")
        time.sleep(7)
        lcd.clear()
if __name__=="__main__":
    main()
