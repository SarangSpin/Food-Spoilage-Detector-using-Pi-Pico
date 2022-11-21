import machine
from machine import I2C, UART
from machine import Pin, ADC
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from sr04 import HCSR04

from dht import DHT11

from micropython import const
from math import exp, log
import utime

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
methane = ADC(26)

bt = UART(0, 9600)
i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

ult = HCSR04(8, 7, 500*2*30)

led = Pin(15, Pin.OUT)

button_next = Pin(18, Pin.IN, Pin.PULL_DOWN)
button_enter = Pin(19, Pin.IN, Pin.PULL_DOWN)
button_prev = Pin(20, Pin.IN, Pin.PULL_DOWN)

pinht= Pin(15, Pin.IN, Pin.PULL_UP)

dht11 = DHT11(pinht,None,dht11=True)

conversion_factor = 3.3 / (65535)
ADC_ConvertedValue = machine.ADC(26)
DIN = Pin(27,Pin.IN)

fruits = ["Apple","Banana","Orange","Mango","Onion","Guava"]
choice = ["Offline","Bluetooth"]
temp = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
R0 = 40500

time = utime.localtime()

if time[3]<12 and time[3]>0:
    lcd.putstr("Hello!\nGood Morning.")
if time[3]<17 and time[3]>12:
    lcd.putstr("Hello!\nGood Afternoon.")
else:
    lcd.putstr("Hello!\nGood Evening.")

utime.sleep(1)
lcd.clear()
utime.sleep(1)
lcd.putstr("Welcome back!")
utime.sleep(2)
lcd.clear()
i=0

while (button_enter.value() == False):
    lcd.putstr("Select the Mode\n")
    lcd.putstr(choice[i])
    utime.sleep(1.3)                          
    if (button_next.value() == True):
        i = i+1
        lcd.clear()
          
    if (button_prev.value() == True):
        i = i-1
        lcd.clear()      
    lcd.clear()
       
     
    
   
utime.sleep(2)

if( i == 0):
    
    if (ult.distance_mm()>80):
        
        lcd.putstr("Fruit\n unavailable")
        
    else:
        j=0
        while (button_enter.value() == False):
             lcd.putstr("Select the fruit\n")
             lcd.putstr(fruits[j])
             utime.sleep(1.3)
             if (button_next.value() == True):
                 j = j+1
                 lcd.clear()
                  
             if (button_prev.value() == True):
                 j = j-1
                 lcd.clear()      
             lcd.clear()
             
    while True:
        T, H = dht11.read()
        print("Temp: " + str(T) + " and " + "Humidity: " + str(H))
        i = 0
        while i<20:
                if(temp[i] == T):
                    p=i
                i = i+1
        AD_value = ADC_ConvertedValue.read_u16() * conversion_factor
        RSL= 33000 / (AD_value)
        RS = RSL - 10000
        l = log(RS/R0)
        v = l - 1.133
        p = v / (0.325)
        x =  0.1**p
        print("The methane in ppm is ",x)
        utime.sleep(0.5)
        
else:
    lcd.backlight_off()
    if bt.any():
        data = str(bt.read())
        if ('start' in data):
            bt.write("Select the fruit\r\n")
            fruit = str(bt.read())
            while True:
                T, H = dht11.read()
                bt.write("Temp : {}\r\n".str(T))
                bt.write("Humidity: {}\r\n".str(H))
                i = 0
                while i<20:
                        if(temp[i] == T):
                            p=i
                        i = i+1
                AD_value = ADC_ConvertedValue.read_u16() * conversion_factor
                RSL= 33000 / (AD_value)
                RS = RSL - 10000
                l = log(RS/R0)
                v = l - 1.133
                p = v / (0.325)
                x =  0.1**p
                bt.write("The methane in ppm is {}\r\n".x)
                utime.sleep(0.5)
                
            
      
    
        
            


