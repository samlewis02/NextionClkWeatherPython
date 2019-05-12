#!/usr/bin/env python

import serial
import datetime
import pytz
import time
import sys
import os
import requests
import re

e = "\xff\xff\xff"
city1 = "London, GB"
city2 = "Kaohsiung, TW"
myplace = city1

def getWeather(placeName):
    url = "http://api.openweathermap.org/data/2.5/weather?q="+ placeName + "&units=metric&APPID=67e5ccb428706c8f055d13402093c432"
    resp = requests.get(url)
    print("Response: "  + str(resp.status_code))
    if resp.status_code == 200 :
        #print(resp.content)
        weath=resp.json()
        ltemp=weath["main"]["temp"]
        lhum=weath["main"]["humidity"]
        lpres=weath["main"]["pressure"]
        lcity=weath["name"]
        lctry=weath["sys"]["country"]
        weather=weath["weather"][0]["main"]
        desc=weath["weather"][0]["description"]
        icon=weath["weather"][0]["icon"]

        print ("Temperature = " + str(ltemp) + "C")
        print ("Humidity = " + str(lhum) + "%RH")
        print ("Pressure = " + str(lpres) + "mBar")
        print ("Location = " + lcity + ", " + lctry)
        print ("Weather = " + weather + ": " + desc)
        print ("Icon = " + str(icon))
        ser.write('place.txt=\"' + str(lcity) + ", " + str(lctry) + '\"' + e)
        ser.write('temp.txt=\"' + str(ltemp) + 'C\"'+ e)
        ser.write('pres.txt=\"' + str(lpres) + 'mBar\"'+ e)
        ser.write('hum.txt=\"' + str(lhum) + '%RH\"'+ e)
        ser.write('desc.txt=\"' + str(desc) + '\"'+ e)
        ser.write('status.txt=\" API data received\"' + e)
    else:
        print("Could not contact host")
        ser.write('status.txt=\" No API data received\"' + e)
   
ser = serial.Serial(
    
    port = '/dev/ttyAMA0',
    baudrate = 9600,
    #stopbits = serial.STOPBITS_ONE,
    #bytesize=serial.EIGHTBITS,
    timeout=5
    )
if serial.VERSION <= "3.0":
    if not ser.isOpen():
        ser.open()
else:
    if not ser.is_open:
        ser.open()
        
getWeather(myplace)

tz1 = pytz.timezone('Europe/London')
tz2 = pytz.timezone('Asia/Taipei')
tz = tz1
rn = datetime.datetime.now(tz)
this_minute = rn.minute
while True:
    if datetime.datetime.now(tz) != rn :
        time = rn.strftime("%H:%M:%S")
        daydate = rn.strftime("%A, %d %B %Y")  
        ser.write('time.txt=\"' + time + '\"'+ e)
        ser.write('daydate.txt=\"' + daydate + '\"'+ e)

        rn = datetime.datetime.now(tz)
        
    if rn.minute == this_minute + 30 :
        getWeather(myplace);
        this_minute = rn.minute
        
    if(ser.inWaiting()>0):
        #print(ser.inWaiting())
        x=str(ser.read_all())
        if "\x08" in x and "\x65" in x:
            print ("change place")
            if myplace == city1:
                myplace = city2
                tz = tz2
            else:
                myplace = city1
                tz = tz1
            getWeather(myplace)
            
