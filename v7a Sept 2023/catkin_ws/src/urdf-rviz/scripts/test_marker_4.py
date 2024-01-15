#!/usr/bin/env python3

# importing required libraries
import roslib; roslib.load_manifest('visualization_marker_tutorials')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import WrenchStamped
from geometry_msgs.msg import Point
import tf2_ros
import tf
import tf_conversions
import rospy
import math
import time
import sys


count = 0
MARKERS_MAX = 1
can_publish = 0

x = 0
y = 0
z = 0

x_rwr = 0
y_rwr = 0
z_rwr = 0

x_ll = 0
y_ll = 0
z_ll = 0

x_rl = 0
y_rl = 0
z_rl = 0


offsetx = 0
offsety = 0
offsetz = 0

offsetx_rwr = 0
offsety_rwr = 0
offsetz_rwr = 0

offsetx_ll = 0
offsety_ll = 0
offsetz_ll = 0

offsetx_rl = 0
offsety_rl = 0
offsetz_rl = 0

final_value_fx_lwr = 0
final_value_fy_lwr = 0
final_value_fz_lwr = 0
final_value_tx_lwr = 0
final_value_ty_lwr = 0
final_value_tz_lwr = 0

final_value_fx_rwr = 0
final_value_fy_rwr = 0
final_value_fz_rwr = 0
final_value_tx_rwr = 0
final_value_ty_rwr = 0
final_value_tz_rwr = 0

final_value_fx_ll = 0
final_value_fy_ll = 0
final_value_fz_ll = 0
final_value_tx_ll = 0
final_value_ty_ll = 0
final_value_tz_ll = 0

final_value_fx_rl = 0
final_value_fy_rl = 0
final_value_fz_rl = 0
final_value_tx_rl = 0
final_value_ty_rl = 0
final_value_tz_rl = 0

set_final_value = 0
set_final_value_rwr = 0
set_final_value_ll = 0
set_final_value_rl = 0

counter = 0
counter_rwr = 0
counter_ll = 0
counter_rl = 0

sensors_visu = [0,0,0,0,0]

#callback for force readings published by left wrist sensor

def wrench_callback_lwr(msg):
	global counter, offsetx,offsety,offsetz,final_value_fx_lwr,final_value_fy_lwr,final_value_fz_lwr,set_final_value,sensors_visu
	global final_value_tx_lwr,final_value_ty_lwr,final_value_tz_lwr
	#print("**********LEFT WRIST**********")
	if(counter==30):
		offsetx = msg.wrench.force.x
		offsety = msg.wrench.force.y
		offsetz = msg.wrench.force.z

	if(offsetx==0):
		pass
	
	else:
		if(sensors_visu[0] == 1):
			final_value_fx_lwr = msg.wrench.force.x - offsetx
			final_value_fy_lwr = msg.wrench.force.y - offsety
			final_value_fz_lwr = msg.wrench.force.z - offsetz
			final_value_tx_lwr = msg.wrench.torque.x
			final_value_ty_lwr = msg.wrench.torque.y
			final_value_tz_lwr = msg.wrench.torque.z
			set_final_value = 1
		else:
			final_value_fx_lwr = 0
			final_value_fy_lwr = 0
			final_value_fz_lwr = 0
			final_value_tx_lwr = 0
			final_value_ty_lwr = 0
			final_value_tz_lwr = 0
			set_final_value = 1
	
	counter = counter + 1

#****************************************************************************************

	
#callback for force readings published by right wrrist sensor

def wrench_callback_rwr(msg_rwr):
	global counter_rwr, offsetx_rwr,offsety_rwr,offsetz_rwr,final_value_fx_rwr,final_value_fy_rwr,final_value_fz_rwr,set_final_value_rwr,sensors_visu
	global final_value_tx_rwr,final_value_ty_rwr,final_value_tz_rwr
	
	
	#print("*****RIGHT WRIST*****")
	
	if(counter_rwr==30):
		offsetx_rwr = msg_rwr.wrench.force.x
		offsety_rwr = msg_rwr.wrench.force.y
		offsetz_rwr = msg_rwr.wrench.force.z

	if(offsetx_rwr==0):
		pass
	
	else:
		if(sensors_visu[1] == 1):
			final_value_fx_rwr = msg_rwr.wrench.force.x - offsetx_rwr
			final_value_fy_rwr = msg_rwr.wrench.force.y - offsety_rwr
			final_value_fz_rwr = msg_rwr.wrench.force.z - offsetz_rwr
			final_value_tx_rwr = msg_rwr.wrench.torque.x
			final_value_ty_rwr = msg_rwr.wrench.torque.y
			final_value_tz_rwr = msg_rwr.wrench.torque.z
			set_final_value_rwr = 1
		else:
			final_value_fx_rwr = 0
			final_value_fy_rwr = 0
			final_value_fz_rwr = 0
			final_value_tx_rwr = 0
			final_value_ty_rwr = 0
			final_value_tz_rwr = 0
			set_final_value_rwr = 1
	
	counter_rwr = counter_rwr + 1

#*****************************************************************************************************

#callback function for readings published by left leg sensor

def wrench_callback_ll(msg_ll):
	global counter_ll, offsetx_ll,offsety_ll,offsetz_ll,final_value_fx_ll,final_value_fy_ll,final_value_fz_ll,set_final_value_ll,sensors_visu
	global final_value_tx_ll,final_value_ty_ll,final_value_tz_ll

	
	#print("*LEFT LEG*")
	
	if(counter_ll==30):
		offsetx_ll = msg_ll.wrench.force.x
		offsety_ll = msg_ll.wrench.force.y
		offsetz_ll = msg_ll.wrench.force.z

	if(offsetx_ll==0):
		pass
	
	else:
		if(sensors_visu[2] == 1):
			#print("Setting final value of right sensor vector")
			final_value_fx_ll = msg_ll.wrench.force.x - offsetx_ll
			final_value_fy_ll = msg_ll.wrench.force.y - offsety_ll
			final_value_fz_ll = msg_ll.wrench.force.z - offsetz_ll
			final_value_tx_ll = msg_ll.wrench.torque.x
			final_value_ty_ll = msg_ll.wrench.torque.y
			final_value_tz_ll = msg_ll.wrench.torque.z
			set_final_value_ll = 1
		else:
			final_value_fx_ll = 0
			final_value_fy_ll = 0
			final_value_fz_ll = 0
			final_value_tx_ll = 0
			final_value_ty_ll = 0
			final_value_tz_ll = 0
			set_final_value_ll = 1
	
	counter_ll = counter_ll + 1

#***************************************************************************************

# callback function for right leg sensor

def wrench_callback_rl(msg_rl):
	global counter_rl, offsetx_rl,offsety_rl,offsetz_rl,final_value_fx_rl,final_value_fy_rl,final_value_fz_rl,set_final_value_rl,sensors_visu
	global final_value_tx_rl,final_value_ty_rl,final_value_tz_rl

	
	#print("*RIGHT LEG*")
	
	if(counter_rl==30):
		offsetx_rl = msg_rl.wrench.force.x
		offsety_rl = msg_rl.wrench.force.y
		offsetz_rl = msg_rl.wrench.force.z

	if(offsetx_rl==0):
		pass
	
	else:
		if(sensors_visu[3] == 1):
			#print("Setting final value of right sensor vector")
			final_value_fx_rl = msg_rl.wrench.force.x - offsetx_rl
			final_value_fy_rl = msg_rl.wrench.force.y - offsety_rl
			final_value_fz_rl = msg_rl.wrench.force.z - offsetz_rl
			final_value_tx_rl = msg_rl.wrench.torque.x
			final_value_ty_rl = msg_rl.wrench.torque.y
			final_value_tz_rl = msg_rl.wrench.torque.z
			set_final_value_rl = 1
		else:
			final_value_fx_rl = 0
			final_value_fy_rl = 0
			final_value_fz_rl = 0
			final_value_tx_rl = 0
			final_value_ty_rl = 0
			final_value_tz_rl = 0
			set_final_value_rl = 1
	
	counter_rl = counter_rl + 1
	
#****************************************************************************************


rospy.init_node('register')

publisher = rospy.Publisher('/visualization_marker_array', MarkerArray, queue_size=10)

rospy.Subscriber("/bus0/ft_sensor0/ft_sensor_readings/wrench", WrenchStamped, wrench_callback_lwr)
rospy.Subscriber("/bus1/ft_sensor1/ft_sensor_readings/wrench", WrenchStamped, wrench_callback_rwr)
rospy.Subscriber("/bus2/ft_sensor2/ft_sensor_readings/wrench", WrenchStamped, wrench_callback_ll)
rospy.Subscriber("/bus3/ft_sensor3/ft_sensor_readings/wrench", WrenchStamped, wrench_callback_rl)

tfbuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfbuffer)

markerArray = MarkerArray()

#callback for wrench function

while not rospy.is_shutdown():

	try:
		trans = tfbuffer.lookup_transform("base_link","l_arm_wr_p", rospy.Time())
		x = trans.transform.translation.x
		y = trans.transform.translation.y
		z = trans.transform.translation.z
		
		trans_rwr = tfbuffer.lookup_transform("base_link","r_arm_wr_p", rospy.Time())
		x_rwr = trans_rwr.transform.translation.x
		y_rwr = trans_rwr.transform.translation.y
		z_rwr = trans_rwr.transform.translation.z
		
		trans_ll = tfbuffer.lookup_transform("base_link","l_leg_an_r", rospy.Time())
		x_ll = trans_ll.transform.translation.x
		y_ll = trans_ll.transform.translation.y
		z_ll = trans_ll.transform.translation.z
		
		trans_rl = tfbuffer.lookup_transform("base_link","r_leg_an_r", rospy.Time())
		x_rl = trans_rl.transform.translation.x
		y_rl = trans_rl.transform.translation.y
		z_rl = trans_rl.transform.translation.z
		print("transform recieved")
		
		can_publish = 1
	except:
		print("Waiting")
		can_publish = 0
	
	#*******************************************************************
	
	#force vector of left wrist
	
	marker_force_lwr = Marker()
	marker_force_lwr.header.frame_id = "base_link"
	marker_force_lwr.type = marker_force_lwr.ARROW
	marker_force_lwr.action = marker_force_lwr.ADD
	marker_force_lwr.scale.x = 0.02
	marker_force_lwr.scale.y = 0.02
	marker_force_lwr.scale.z = 0.02
	marker_force_lwr.color.a = 1.0
	marker_force_lwr.color.r = 1.0
	marker_force_lwr.color.g = 0.0
	marker_force_lwr.color.b = 0.0
	marker_force_lwr.pose.orientation.w = 1.0
	
	
	start_point_lwr = Point()
	start_point_lwr.x = x
	start_point_lwr.y = y
	start_point_lwr.z = z
	end_point_lwr = Point()
	end_point_lwr.x = (x + (final_value_fx_lwr/10))
	end_point_lwr.y = (y + (final_value_fy_lwr/10))
	end_point_lwr.z = (z + (final_value_fz_lwr/10))
	marker_force_lwr.points = [start_point_lwr,end_point_lwr] 
	
	#*******************************************************************

	#torque vector for left wrist
	
	torque_marker_lwr = Marker()
	torque_marker_lwr.header.frame_id = "base_link"
	torque_marker_lwr.type = torque_marker_lwr.ARROW
	torque_marker_lwr.action = torque_marker_lwr.ADD
	torque_marker_lwr.scale.x = 0.02
	torque_marker_lwr.scale.y = 0.02
	torque_marker_lwr.scale.z = 0.02
	torque_marker_lwr.color.a = 1.0
	torque_marker_lwr.color.r = 0.0
	torque_marker_lwr.color.g = 1.0
	torque_marker_lwr.color.b = 0.0
	torque_marker_lwr.pose.orientation.w = 1.0
	
	
	start_point_lwr_torque = Point()
	start_point_lwr_torque.x = x
	start_point_lwr_torque.y = y
	start_point_lwr_torque.z = z
	end_point_lwr_torque = Point()
	end_point_lwr_torque.x = (x + (final_value_tx_lwr/10))
	end_point_lwr_torque.y = (y + (final_value_ty_lwr/10))
	end_point_lwr_torque.z = (z + (final_value_tz_lwr/10))
	torque_marker_lwr.points = [start_point_lwr_torque,end_point_lwr_torque] 
	
	
	#*******************************************************************
	
	#force vector of right wrist
	
	marker_force_rwr = Marker()
	marker_force_rwr.header.frame_id = "base_link"
	marker_force_rwr.type = marker_force_rwr.ARROW
	marker_force_rwr.action = marker_force_rwr.ADD
	marker_force_rwr.scale.x = 0.02
	marker_force_rwr.scale.y = 0.02
	marker_force_rwr.scale.z = 0.02
	marker_force_rwr.color.a = 1.0
	marker_force_rwr.color.r = 1.0
	marker_force_rwr.color.g = 0.0
	marker_force_rwr.color.b = 0.0
	marker_force_rwr.pose.orientation.w = 1.0
	
	
	start_point_rwr = Point()
	start_point_rwr.x = x_rwr
	start_point_rwr.y = y_rwr
	start_point_rwr.z = z_rwr
	end_point_rwr = Point()
	end_point_rwr.x = (x_rwr + (final_value_fx_rwr/10))
	end_point_rwr.y = (y_rwr + (final_value_fy_rwr/10))
	end_point_rwr.z = (z_rwr + (final_value_fz_rwr/10))
	marker_force_rwr.points = [start_point_rwr,end_point_rwr] 
	
	#*******************************************************************

	#torque vector for right wrist
	
	torque_marker_rwr = Marker()
	torque_marker_rwr.header.frame_id = "base_link"
	torque_marker_rwr.type = torque_marker_rwr.ARROW
	torque_marker_rwr.action = torque_marker_rwr.ADD
	torque_marker_rwr.scale.x = 0.02
	torque_marker_rwr.scale.y = 0.02
	torque_marker_rwr.scale.z = 0.02
	torque_marker_rwr.color.a = 1.0
	torque_marker_rwr.color.r = 0.0
	torque_marker_rwr.color.g = 1.0
	torque_marker_rwr.color.b = 0.0
	torque_marker_rwr.pose.orientation.w = 1.0
	
	
	start_point_rwr_torque = Point()
	start_point_rwr_torque.x = x_rwr
	start_point_rwr_torque.y = y_rwr
	start_point_rwr_torque.z = z_rwr
	end_point_rwr_torque = Point()
	end_point_rwr_torque.x = x_rwr#(x_rwr + (final_value_tx_rwr))
	end_point_rwr_torque.y = y_rwr#(y_rwr + (final_value_ty_rwr))
	end_point_rwr_torque.z = z_rwr#(z_rwr + (final_value_tz_rwr))
	torque_marker_rwr.points = [start_point_rwr_torque,end_point_rwr_torque] 
	
	
	#*******************************************************************
	
	#force vector of left leg
	
	marker_force_ll = Marker()
	marker_force_ll.header.frame_id = "base_link"
	marker_force_ll.type = marker_force_ll.ARROW
	marker_force_ll.action = marker_force_ll.ADD
	marker_force_ll.scale.x = 0.02
	marker_force_ll.scale.y = 0.02
	marker_force_ll.scale.z = 0.02
	marker_force_ll.color.a = 1.0
	marker_force_ll.color.r = 1.0
	marker_force_ll.color.g = 0.0
	marker_force_ll.color.b = 0.0
	marker_force_ll.pose.orientation.w = 1.0
	
	
	start_point_ll = Point()
	start_point_ll.x = x_ll
	start_point_ll.y = y_ll
	start_point_ll.z = z_ll
	end_point_ll = Point()
	end_point_ll.x = (x_ll + (final_value_fx_ll/10))
	end_point_ll.y = (y_ll + (final_value_fy_ll/10))
	end_point_ll.z = (z_ll + (final_value_fz_ll/10))
	marker_force_ll.points = [start_point_ll,end_point_ll] 
	
	#*******************************************************************

	#torque vector for left leg 
	
	torque_marker_ll = Marker()
	torque_marker_ll.header.frame_id = "base_link"
	torque_marker_ll.type = torque_marker_ll.ARROW
	torque_marker_ll.action = torque_marker_ll.ADD
	torque_marker_ll.scale.x = 0.02
	torque_marker_ll.scale.y = 0.02
	torque_marker_ll.scale.z = 0.02
	torque_marker_ll.color.a = 1.0
	torque_marker_ll.color.r = 0.0
	torque_marker_ll.color.g = 1.0
	torque_marker_ll.color.b = 0.0
	torque_marker_ll.pose.orientation.w = 1.0
	
	
	start_point_ll_torque = Point()
	start_point_ll_torque.x = x_ll
	start_point_ll_torque.y = y_ll
	start_point_ll_torque.z = z_ll
	end_point_ll_torque = Point()
	end_point_ll_torque.x = x_ll#(x_ll + (final_value_tx_ll))
	end_point_ll_torque.y = y_ll#(y_ll + (final_value_ty_ll))
	end_point_ll_torque.z = z_ll#(z_ll + (final_value_tz_ll))
	torque_marker_ll.points = [start_point_ll_torque,end_point_ll_torque] 
	
	#*******************************************************************
	
	#*******************************************************************
	
	#force vector of right leg
	
	marker_force_rl = Marker()
	marker_force_rl.header.frame_id = "base_link"
	marker_force_rl.type = marker_force_rl.ARROW
	marker_force_rl.action = marker_force_rl.ADD
	marker_force_rl.scale.x = 0.02
	marker_force_rl.scale.y = 0.02
	marker_force_rl.scale.z = 0.02
	marker_force_rl.color.a = 1.0
	marker_force_rl.color.r = 1.0
	marker_force_rl.color.g = 0.0
	marker_force_rl.color.b = 0.0
	marker_force_rl.pose.orientation.w = 1.0
	
	
	start_point_rl = Point()
	start_point_rl.x = x_rl
	start_point_rl.y = y_rl
	start_point_rl.z = z_rl
	end_point_rl = Point()
	end_point_rl.x = (x_rl + (final_value_fx_rl/10))
	end_point_rl.y = (y_rl + (final_value_fy_rl/10))
	end_point_rl.z = (z_rl + (final_value_fz_rl/10))
	marker_force_rl.points = [start_point_rl,end_point_rl] 
	
	#*******************************************************************

	#torque vector for right leg 
	
	torque_marker_rl = Marker()
	torque_marker_rl.header.frame_id = "base_link"
	torque_marker_rl.type = torque_marker_rl.ARROW
	torque_marker_rl.action = torque_marker_rl.ADD
	torque_marker_rl.scale.x = 0.02
	torque_marker_rl.scale.y = 0.02
	torque_marker_rl.scale.z = 0.02
	torque_marker_rl.color.a = 1.0
	torque_marker_rl.color.r = 0.0
	torque_marker_rl.color.g = 1.0
	torque_marker_rl.color.b = 0.0
	torque_marker_rl.pose.orientation.w = 1.0
	
	
	start_point_rl_torque = Point()
	start_point_rl_torque.x = x_rl
	start_point_rl_torque.y = y_rl
	start_point_rl_torque.z = z_rl
	end_point_rl_torque = Point()
	end_point_rl_torque.x = x_rl#(x_rl + (final_value_tx_rl))
	end_point_rl_torque.y = y_rl#(y_rl + (final_value_ty_rl))
	end_point_rl_torque.z = z_rl#(z_rl + (final_value_tz_rl))
	torque_marker_rl.points = [start_point_rl_torque,end_point_rl_torque] 
	
	#*******************************************************************
	
	# We add the new marker to the MarkerArray, removing the oldest
	# marker from it when necessary
	if(count > MARKERS_MAX):
		markerArray.markers.pop(0)
		markerArray.markers.pop(0)
		markerArray.markers.pop(0)
		markerArray.markers.pop(0)
		markerArray.markers.pop(0)
		markerArray.markers.pop(0)
		markerArray.markers.pop(0)
		markerArray.markers.pop(0)

	markerArray.markers.append(marker_force_lwr)
	markerArray.markers.append(torque_marker_lwr)
	markerArray.markers.append(marker_force_rwr)
	markerArray.markers.append(torque_marker_rwr)
	markerArray.markers.append(marker_force_ll)
	markerArray.markers.append(torque_marker_ll)
	markerArray.markers.append(marker_force_rl)
	markerArray.markers.append(torque_marker_rl)

	# Renumber the marker IDs
	id = 0
	for m in markerArray.markers:
		m.id = id
		id += 1
	time.sleep(0.05)
	with open("/home/robotis/catkin_ws/src/shared_variable.txt", "r") as file:
		a = str(file.read())
		
	#print(f"The value of list are: {int(a[1])} {int(a[4])} {int(a[7])} {int(a[10])} {int(a[13])}")
	try:
		sensors_visu = [int(a[1]),int(a[4]),int(a[7]),int(a[10]), int(a[13])]
	except:
		pass
	
	#publishing the values
	if((can_publish == 1) and (set_final_value == 1) and (set_final_value_rwr==1) and (set_final_value_rl==1)):
		publisher.publish(markerArray)
		print(f"**********{len(markerArray.markers)}**********")
	else:
		print("not publishing")
		
	count += 8
	rospy.sleep(0.01)

