import serial
import time

ser=serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=8.0)
hello=port.read(100)
if hello!="":
	echo(hello)
else:
	echo("Error")
ser.close()
