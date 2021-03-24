import time
import serial
import pynmea2

#ser = serial.Serial(port = '/dev/serial0', baudrate =9600, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
ser = serial.Serial('/dev/serial0',9600)
n = 1
while (n==1):
    x = ser.readline()
    #print(x)
    gpgga3b = bytes("$GNVTG", 'utf-8')
    gpgga2b = bytes("$GNGGA", 'utf-8')
    
    if(x.startswith(gpgga3b)):
        mes2 = pynmea2.parse(x.decode('ascii',errors='replace'))
        speedog = (mes2.spd_over_grnd_kmph)
        print(speedog) # first value  
    elif(x.startswith(gpgga2b)):
        mes = pynmea2.parse(x.decode('ascii',errors='replace'))
        longog = (mes.longitude)
        latog = (mes.latitude)
        altog = (mes.altitude)
        print(longog) # second value 
        print(latog) # third value
        print(altog) # fourth value
        n = 0
    