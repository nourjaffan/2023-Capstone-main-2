#!/usr/bin/env python3

import rospy
import math

import os
from dynamixel_sdk import *
from dynamixel_sdk_examples.srv import *
from dynamixel_sdk_examples.msg import *
from getch import *
import time
import ctypes

from tf.transformations import euler_from_quaternion, quaternion_from_euler

ADDR_TORQUE_ENABLE    = 512 
ADDR_PRESENT_POSITION = 580
ADDR_GOAL_POSITION = 564
ADDR_VELOCITY_LIMIT = 44

DEVICENAME0 = '/dev/ttyUSB0' #Specify whatever port the motors are connected to

TORQUE_ENABLE  = 1               # Value for enabling the torque
TORQUE_DISABLE = 0               # Value for disabling the torque

PROTOCOL_VERSION = 2.0

BAUDRATE = 1000000

portHandler = PortHandler(DEVICENAME0)
packetHandler = PacketHandler(PROTOCOL_VERSION)

def set_velocity_limit(motor_id,limit):
    
    global portHandler
    global packetHandler

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, motor_id, ADDR_VELOCITY_LIMIT, limit)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        print("Press any key to terminate...")
        getch()
        quit()
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("Press any key to terminate...")
        getch()
        quit()
    else:
        print(f"DYNAMIXEL ID : {motor_id} Velocity set : {limit}")

def init_motor(motor_id,en):
    
    global portHandler
    global packetHandler

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_TORQUE_ENABLE, en)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        print("Press any key to terminate...")
        getch()
        quit()
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("Press any key to terminate...")
        getch()
        quit()
    else:
        if(en==1):
            print(f"DYNAMIXEL ID : {motor_id} has been successfully connected")
        elif(en==0):
            print(f"DYNAMIXEL ID : {motor_id} has been successfully disconnected")


def write_angle(motor_id,value):

    global packetHandler
    global portHandler

    ph42_coeff = 607500/360
    ph54_coeff = 501433/180

    if(motor_id < 9):
        k = ph54_coeff
    else:
        k = ph42_coeff 

    #print(f"Changing ID : {motor_id} to angle : {angle} degrees")
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, motor_id, ADDR_GOAL_POSITION, value)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        print("Press any key to terminate...")
        getch()
        quit()
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("Press any key to terminate...")
        getch()
        quit()
    else:
       print(f"DYNAMIXEL ID : {motor_id} changed to {value} ")

def say_hi():    
    write_angle(2,-27907)
    time.sleep(0.35)
    write_angle(8,208567)
    #time.sleep(6)
    write_angle(12,140296)
    #time.sleep(6)
    write_angle(14,150657)
    time.sleep(4)
    write_angle(10,22111)
    time.sleep(0.3)
    write_angle(10,-22111)
    time.sleep(1)
    write_angle(10,22111)
    time.sleep(1)
    write_angle(10,-22111)
    time.sleep(1)
    write_angle(10,0)
    time.sleep(1.25)
    write_angle(14,0)
    #time.sleep(6)
    write_angle(12,0)
    #time.sleep(6)
    write_angle(8,0)
    time.sleep(4)
    write_angle(2,0)
    time.sleep(3)

rospy.init_node('demo_script_node', anonymous=True)

portHandler.openPort()
portHandler.setBaudRate(BAUDRATE)

for i in  range (2,15,2):
    set_velocity_limit(i,500)
    init_motor(i,1)
time.sleep(5)



say_hi()
for i in  range (2,15,2):
    init_motor(i,0)


