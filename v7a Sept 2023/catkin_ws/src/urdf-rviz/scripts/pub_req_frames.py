#!/usr/bin/env python3

import rospy
import tf2_ros
import tf
import tf_conversions
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import time

position = [0,0,0]
rpy_quaternion = [0,0,0,1]
gyro_value = [0,0,0]
accel_value = [0,0,0]
offset_base_lidar_link = [0,0,1]
odom_msg = Odometry()
imu_msg = Imu()
cov = [0,0,0]
#odometry callback : published by the intelrealsense T265 camera

def odom_callback(msg):
    global position, rpy_quaternion,odom_msg,cov
    
    odom_msg = msg

    position[0] = msg.pose.pose.position.x
    position[1] = msg.pose.pose.position.y
    position[2] = msg.pose.pose.position.z

    rpy_quaternion[0] = msg.pose.pose.orientation.x
    rpy_quaternion[1] = msg.pose.pose.orientation.y
    rpy_quaternion[2] = msg.pose.pose.orientation.z
    rpy_quaternion[3] = msg.pose.pose.orientation.w
    
    #print(f"Position : {position} \t Orientation {rpy_quaternion}")

def gyro_callback(msg):
    global gyro_value, imu_msg, accel_value, rpy_quaternion
    gyro_value[0] = msg.angular_velocity.x
    gyro_value[1] = msg.angular_velocity.z
    gyro_value[2] = msg.angular_velocity.y
    imu_msg = msg

    imu_msg.orientation.x = rpy_quaternion[0]
    imu_msg.orientation.y = rpy_quaternion[1]
    imu_msg.orientation.z = rpy_quaternion[2]
    imu_msg.orientation.w = rpy_quaternion[3]

    imu_msg.linear_acceleration.x = accel_value[0]
    imu_msg.linear_acceleration.z = accel_value[1]
    imu_msg.linear_acceleration.y = accel_value[2]
    
    imu_msg.header.frame_id = "imu_link" #print(f"\n{imu_msg}\n")

def accel_callback(msg):
    global accel_value
    accel_value[0] = msg.linear_acceleration.x
    accel_value[1] = msg.linear_acceleration.y
    accel_value[2] = msg.linear_acceleration.z


rospy.init_node("publish_tfs")
rospy.Subscriber("/camera/odom/sample",Odometry,odom_callback)
rospy.Subscriber("/camera/gyro/sample",Imu,gyro_callback)
rospy.Subscriber("/camera/accel/sample",Imu,accel_callback)
pub_imu = rospy.Publisher("/my_imu",Imu,queue_size=10)
pub_odom = rospy.Publisher("/odom",Odometry,queue_size=10)

#Publishing the transforms mentioned in the hector slam ros documentation

br = tf.TransformBroadcaster()

while not rospy.is_shutdown():
    #br.sendTransform((position[0],position[1],0),tuple(rpy_quaternion),rospy.Time.now(),"base_link_footprint","odom")
    br.sendTransform(tuple(position),tuple(rpy_quaternion),rospy.Time.now(),"base_link","odom")
    #br.sendTransform(tuple(position),tuple(rpy_quaternion),rospy.Time.now(),"imu_link","base_link")
    #br.sendTransform(tuple(position),tuple(rpy_quaternion),rospy.Time.now(),"camera_pose_frame","odom")
    #br.sendTransform(tuple(position),(0,0,0,1),rospy.Time.now(),"base_stabilised","odom")
    br.sendTransform((offset_base_lidar_link[0],offset_base_lidar_link[1],offset_base_lidar_link[2]),(0,0,0,1),rospy.Time.now(),"velodyne","base_link")

    
    time.sleep(0.01)
    pub_imu.publish(imu_msg)
    pub_odom.publish(odom_msg)





