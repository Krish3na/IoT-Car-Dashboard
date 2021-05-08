import time
import RPi.GPIO as GPIO
from RPLCD import CharLCD
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23],numbering_mode=GPIO.BCM)

while True:
    print("Hello World!")
    lcd.write_string(u"Hello world!")
    time.sleep(4)
    lcd.clear()
    time.sleep(4)
