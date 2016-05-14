# BtCtrPi

Python Libraries needed:
smbus
math
numpy 
time
serial


getvalues.py Fetches data from MPU60X0, filters data (Kalman filter and Mechanical filter) and takes away calibration's value.
Just started, Sorry for few documentation but i have just started.

alpha version: 
2 raspberry 3, one fetches data through i2c from IMU elaborates them and sends them over bluetooth connection to the other Pi, which is connected through serial port to Comau Robot, which will receive accelerometer data and move accordingly.

Problems: rasp needed where computations are done, due to high complexity of kalman filter implemented(i know less complex filter could have been implemented). I'd wire the rasp with the comau robot, and use an arduino nano like microcontroller to fetch the data from imu and send to pi over bluetooth, will i get enough measurements for the filter in a quiet small time?? or bluetooth transfer will make me waste too much time. for the time being i'll use two rasp and just avoid this problem. After i'll need to solve it. 
