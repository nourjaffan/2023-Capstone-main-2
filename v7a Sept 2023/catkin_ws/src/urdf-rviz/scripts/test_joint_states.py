#!/usr/bin/env python3

import rospy
import time
import math
import os
import tf2_ros
import tf
import tf_conversions
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Point

from sensor_msgs.msg import JointState
rospy.init_node('send_joint_states', anonymous=True)
pub = rospy.Publisher('joint_states',JointState,queue_size = 10)

#Killing the fake joint_state_publisher
os.system("rosnode kill /joint_state_publisher")

#Adding each joint to the list of joints
msg = JointState()
msg.name.append('r_arm_sh_p1_joint')
msg.name.append('r_arm_sh_r_joint')
msg.name.append('r_arm_sh_p2_joint')
msg.name.append('r_arm_el_y_joint')
msg.name.append('r_arm_wr_r_joint')
msg.name.append('r_arm_wr_y_joint')
msg.name.append('r_arm_wr_p_joint')
msg.name.append('r_arm_grip_thumb_joint')
msg.name.append('r_arm_grip_index_joint')
msg.name.append('r_arm_grip_middle_joint')

msg.name.append('l_arm_sh_p1_joint')
msg.name.append('l_arm_sh_r_joint')
msg.name.append('l_arm_sh_p2_joint')
msg.name.append('l_arm_el_y_joint')
msg.name.append('l_arm_wr_r_joint')
msg.name.append('l_arm_wr_y_joint')
msg.name.append('l_arm_wr_p_joint')
msg.name.append('l_arm_grip_thumb_joint')
msg.name.append('l_arm_grip_index_joint')
msg.name.append('l_arm_grip_middle_joint')

for x in range(20):
	msg.position.append(0.0)

msg.velocity = []
msg.effort = []
tfbuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfbuffer)
angle = 0
angle2 = 0
br = tf.TransformBroadcaster()
br2 = tf.TransformBroadcaster()
br3 = tf.TransformBroadcaster()
markerArray = MarkerArray()
count = 0
while(1):
	msg.position[0] = angle
	angle = angle + 0.01
	msg.header.stamp = rospy.Time.now()
	msg.header.seq += 1
	pub.publish(msg)
	print("\n")
	try:
		trans = tfbuffer.lookup_transform("map","r_arm_wr_p", rospy.Time())
		print("Success")
	except:
		print("Failed")

