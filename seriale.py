#!/usr/bin/env python
import time
import serial
import getvalues as gv
      
	ser = serial.Serial(
              
        	port='/dev/ttyAMA0',
      		baudrate = 9600,
        	parity=serial.PARITY_NONE,
        	stopbits=serial.STOPBITS_ONE,
        	bytesize=serial.EIGHTBITS,
        	timeout=1
        )
        counter=0
        while counter<200:
		data=gv.getValues()
		if len(data) != 0:
        		ser.write('%s'%data)
		        counter += 1
               	time.sleep(1)
