#!/usr/bin/python
import smbus
import math
import numpy as np
import time
import serial

#instatiate serial object
ser = serial.Serial(
	
	port = '/dev/ttyAMA0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout=1
)
# Power management registers

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
#define kalman filter class
class Kalman:
    def __init__(self,init_value,dir):
        self.q = 0.0625
        self.r = 4
	self.p = 1.3833094
	self.x = init_value
	self.k = 0
	self.direction=dir
	y=0
	self.calibrated=0
	start2=time.time()
	while y < 1023:
		if self.direction == 0:
			self.calibrated=self.calibrated+read_word_2c(0x03b)
		if self.direction == 1:
			self.calibrated=self.calibrated+read_word_2c(0x03d)
		if self.direction == 2:
			self.calibrated=self.calibrated+read_word_2c(0x03f)			
		y=y+1
	self.calibrated=self.calibrated/y
	print "calibration time %s" % (time.time()-start2)
    def update(self,measX):
#prediction update of kalman Filter
	self.p = self.p + self.q
#measurement update
	self.k = self.p/(self.p + self.r)
	self.x = self.x + self.k*(measX - self.x)
	self.p = (1 - self.k)*self.p
	return self.x
#define MPU60X0 read functions
def read_byte(adr):

    return bus.read_byte_data(address, adr)
 
def read_word(adr):

    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val
	 
def read_word_2c(adr):

    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
	 
def dist(a,b):

    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):

    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):

    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

 
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
	 
#print "gyro data"
#print "---------"

def getfilteredvalues(kalx,kaly,kalz):
	 
	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)

	gyro_xout_scaled = gyro_xout / 131
	gyro_yout_scaled = gyro_yout / 131
	gyro_zout_scaled = gyro_zout / 131
	 
#print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
#print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
#print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)
	 
#print
#print "accelerometer data"
#print "------------------"

	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)
	 
	accel_xout_scaled = accel_xout / 16384.0
	accel_yout_scaled = accel_yout / 16384.0
	accel_zout_scaled = accel_zout / 16384.0
#print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
#print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
#print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
#print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
#print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

	start_time=time.time()
#updating kalman filter
	for y in range (0,127):
	
		measx=read_word_2c(0x03b)/16384.0
		measy=read_word_2c(0x3d)/16384.0
		measz=read_word_2c(0x3f)/16384.0

		measx=kalx.update(measx)
		measy=kaly.update(measy)
		measz=kalz.update(measz)
#deleting offset/calibration value
	measx=measx-kalx.calibrated
	measy=measy-kaly.calibrated
	measz=measz-kalz.calibrated
#mechanical filter implementation	
	if measx < 0.2:
		measx=0
	if measy < 0.2:
		measy=0
	if measz < 0.2:
		measz=0
#print execution time and ready values

	print("--- %s seconds ---" %(time.time()-start_time))
	print "x acceleration filtered:%f"%measx
	print "y acceleretion filtered:%f"%measy
	print "z acceleration filtered:%f"%measz

kalx=Kalman(read_word_2c(0x03b)/16384,0)
kaly=Kalman(read_word_2c(0x03d)/16384,1)
kalz=Kalman(read_word_2c(0x03f)/16384,2)
getfilteredvalues(kalx,kaly,kalz)
