import subprocess
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder

from kivymd.uix.tab import MDTabsBase
from kivy.uix.dropdown import DropDown
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
import urllib.request
from kivy.clock import mainthread
from kivymd.app import MDApp
import time
import rospy
from geometry_msgs.msg import WrenchStamped

from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Int64
import math

import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

visualising_ft_sensors = [0,0,0,0,0]
lw = 0
rw = 0
ll = 0
rl = 0
lwrb = 0
rwrb = 0
llrb = 0
rlrb = 0
subscriber = 0
create_node = 0
subscribed_to_some_topic = 0
KV = """
<MenuScreen>:
	name: 'home'
	img: asyn_image
	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "[b]Humanoid Control Panel[/b]"
			anchor_title: "center"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["engine", lambda x: app.callback(x)], ["robot-confused-outline", lambda x: app.set_screen('id')], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		AsyncImage:
			id: asyn_image
			source: root.image_path
			size_hint: None, None
			width: 400
			height: 400
			pos_hint: {'center_x':.5, 'center_y': .5}
			nocache: True
		
		MDLabel:
			text: "Transcend Humanoid Robot GUI"
			pos_hint: {"center_x": 0.8, "center_y": 0.8}
			font_size: 22
			bold: True

		# Button:
		# 	id: refresh_btn
		# 	text: "Refresh"
		# 	halign: "center"
		# 	size_hint: 0.15, 0.1
		# 	pos_hint: {"center_x": .5, "center_y": 0.5}
		# 	on_press: root.change_image("new_robotImage.png")

		# Button:
		# 	id: run_btn
		# 	text: "Run"
		# 	halign: "center"
		# 	size_hint: 0.15, 0.1
		# 	pos_hint: {"center_x": .1, "center_y": 0.2}
		
		Button:
			id: emergency
			text: "EM-STOP"
			halign: "center"
			background_color: get_color_from_hex('#FF0A01')
			#background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .5, "center_y": 0.15}
			on_press: app.emergency_stop()

		# Button:
		# 	id: btn 
		# 	text: "Load Demo:"
		# 	halign: "center"
		# 	size_hint: 0.25, 0.1
		# 	pos_hint: {"center_x": .65, "center_y": 0.8}
		# 	on_parent: drop_content.dismiss()
		# 	on_release: drop_content.open(self)

		# DropDown:
		# 	id: drop_content
		# 	on_select: btn.text = '{}'.format(args[1])

		# 	Button:
		# 		id: btn1
		# 		text: 'First Item'
		# 		size_hint_y: None
		# 		height: 35
		# 		on_release: drop_content.select('First Item')
			
		# 	Button:
		# 		id: btn2
		# 		text: 'Second Item'
		# 		size_hint_y: None
		# 		height: 35
		# 		on_release: drop_content.select('Second Item')

		# FloatLayout:
		# 	MDRaisedButton:
		# 		id: caller
		# 		text: "Motor Selection"
		# 		pos_hint: {"center_x": .75, "center_y": .5}
		# 		on_release: app.menu.open()
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				icon: 'cog'

<MenuLeftArmScreen>:
	name: 'home_leftarm_control'
	img: la_asyn_image
	m1_pos_slider: m1_slider
	m2_pos_slider: m2_slider
	m3_pos_slider: m3_slider
	m4_pos_slider: m4_slider
	m5_pos_slider: m5_slider
	m6_pos_slider: m6_slider
	m7_pos_slider: m7_slider
	m8_pos_slider: m8_slider
	m9_pos_slider: m9_slider
	m10_pos_slider: m10_slider

	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "[b]Humanoid Control Panel[/b]"
			anchor_title: "center"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["engine", lambda x: app.callback(x)], ["robot-confused-outline", lambda x: app.set_screen('id')], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		AsyncImage:
			id: la_asyn_image
			source: root.image_path
			size_hint: None, None
			width: 400
			height: 400
			pos_hint: {'center_x':.25, 'center_y': .6}
			nocache: True

		Button:
			id: run_btn
			text: "RUN"
			background_normal: ''
			background_color: rgba("#00ab66")
			color:0,0,0,1
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .19, "center_y": 0.2}
		
		Button:
			id: emergency
			text: "EM-STOP"
			background_normal: ''
			background_color: rgba("#ff0a01")
			color:0,0,0,1
			halign: "center"
			# background_color: get_color_from_hex('#FF0A01')
			# background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .35, "center_y": 0.2}
			on_press: app.emergency_stop()

		FloatLayout:
			#pos_hint: {"right": 1}
			# size_hint: 0.5, 0.5
			GridLayout:
				pos_hint: {"center_x": 0.5, "center_y": 0.4}
				col_default_width: '56dp'
				size_hint_x: None
				cols: 8
				row_default_height: '32dp'
				size_hint_y: None
				height: self.minimum_height
				Label:
					bold: True
					font_size: '10sp'
					text: 'SENSOR'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'ID'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'POS CTRL' 
					color: (0,0,0,1)		   
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL POS'  
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'CUR POS'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'VEL CTRL'
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL VEL' 
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'SEND'
					color: (0,0,0,1)
				# Motor 1
				CheckBox:
					id: m1_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m1_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '2'
					id: m1_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m1_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m1_command_callback()
					#size_hint:(None, .5)
					#width: 200

				TextInput:
					id: m1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m1_slider.value)
				Label:
					text: str(m1_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				# MDFloatingActionButton:
				#	 id: m1_minusbutton
				#	 icon: "minus"
				#	 size_hint: 0.025, 0.03
				#	 pos_hint: {"center_x": .225, "center_y": 0.5}
				#	 pos: 10, 10
				#	 on_release: app.callback()

				# MDFloatingActionButton:
				#	 id: m1_plusbutton
				#	 icon: "plus"
				#	 size_hint: 0.025, 0.03
				#	 pos_hint: {"center_x": .25, "center_y": 0.5}
				#	 pos: 10, 10
				#	 on_release: app.callback()
				Slider:
					id: velo1_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo1_slider.value)
				# Label:
				#	 text: str(velo_slider.value)
				#	 color: (0,0,1,1)
				#	 canvas.before:
				#		 Color:
				#			 rgba: 1, 1, 1, 1
				#		 Rectangle:
				#			 pos: self.pos
				#			 size: self.size

				Button:
					id: pub1
					text: 'Pub'
					on_press:app.send_position(m1_id.text, m1_slider.value, velo1_slider.value, "pub1") 
				# Motor 2
				CheckBox:
					id: m2_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m2_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '4'
					id: m2_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m2_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m2_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m2_slider.value)
				Label:
					text: str(m2_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo2_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo2_slider.value)						
				Button:
					id: pub2
					text: 'Pub'
					on_press:app.send_position(m2_id.text, m2_slider.value, velo2_slider.value, "pub2")

				# Motor 3
				CheckBox:
					id: m3_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m3_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '6'
					id: m3_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m3_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m3_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m3_slider.value)
				Label:
					text: str(m3_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo3_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo3_slider.value)						   
				Button:
					id: pub3
					text: 'Pub'
					on_press:app.send_position(m3_id.text, m3_slider.value, velo3_slider.value, "pub3")

				# Motor 4
				CheckBox:
					id: m4_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m4_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '8'
					id: m4_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m4_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m4_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m4_slider.value)
				Label:
					text: str(m4_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo4_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo4_slider.value)						   
				Button:
					id: pub4
					text: 'Pub'
					on_press:app.send_position(m4_id.text, m4_slider.value, velo4_slider.value, "pub4")

				# Motor 5
				CheckBox:
					id: m5_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m5_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '10'
					id: m5_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m5_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m5_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m5_slider.value)
				Label:
					text: str(m5_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo5_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo5_slider.value)						   
				Button:
					id: pub5
					text: 'Pub'
					on_press:app.send_position(m5_id.text, m5_slider.value, velo5_slider.value, "pub5")

				# Motor 6
				CheckBox:
					id: m6_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m6_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '12'
					id: m6_id
					color: (0,0,1,1)
					size_hint_x: .40
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m6_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m6_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m6_slider.value)
				Label:
					text: str(m6_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo6_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo6_slider.value)						   
				Button:
					id: pub6
					text: 'Pub'
					on_press:app.send_position(m6_id.text, m6_slider.value, velo6_slider.value, "pub6")

				# Motor 7
				CheckBox:
					id: m7_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m7_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '14'
					id: m7_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m7_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m7_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m7_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m7_slider.value)
				Label:
					text: str(m7_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo7_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo7_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo7_slider.value)						   
				Button:
					id: pub7
					text: 'Pub'
					on_press:app.send_position(m7_id.text, m7_slider.value, velo7_slider.value, "pub7")

				#hand motors
				CheckBox:
					id: m8_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m8_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '32'
					id: m8_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m8_slider
					value: 0
					min: 0
					max: 5
					step: 1
					on_touch_up: root.m8_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m8_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m8_slider.value)
				Label:
					text: str(m8_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo8_slider
					value: 150
					min: 1
					max: 380
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo8_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo8_slider.value)						  
				Button:
					id: pub8
					text: 'Pub'
					on_press:app.send_position(m8_id.text, m8_slider.value, velo8_slider.value, "pub8")
				
				CheckBox:
					id: m9_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m9_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '34'
					id: m9_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m9_slider
					value: 0
					min: 0
					max: 5
					step: 1
					on_touch_up: root.m9_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m9_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m9_slider.value)
				Label:
					text: str(m9_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo9_slider
					value: 150
					min: 1
					max: 380
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo9_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo9_slider.value)						  
				Button:
					id: pub9
					text: 'Pub'
					on_press:app.send_position(m9_id.text, m9_slider.value, velo9_slider.value, "pub9")

				
				CheckBox:
					id: m10_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m10_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '36'
					id: m10_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m10_slider
					value: 0
					min: 0
					max: 5
					step: 1
					on_touch_up: root.m10_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m10_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m10_slider.value)
				Label:
					text: str(m10_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo10_slider
					value: 150
					min: 1
					max: 380
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo10_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo10_slider.value)						  
				Button:
					id: pub10
					text: 'Pub'
					on_press:app.send_position(m10_id.text, m10_slider.value, velo10_slider.value, "pub10")
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				icon: 'cog'

<MenuRightArmScreen>:
	name: 'home_rightarm_control'
	img: ra_asyn_image
	m1_pos_slider: m1_slider
	m2_pos_slider: m2_slider
	m3_pos_slider: m3_slider
	m4_pos_slider: m4_slider
	m5_pos_slider: m5_slider
	m6_pos_slider: m6_slider
	m7_pos_slider: m7_slider
	m8_pos_slider: m8_slider
	m9_pos_slider: m9_slider
	m10_pos_slider: m10_slider

	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "[b]Humanoid Control Panel[/b]"
			anchor_title: "center"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["engine", lambda x: app.callback(x)], ["robot-confused-outline", lambda x: app.set_screen('id')], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		AsyncImage:
			id: ra_asyn_image
			source: root.image_path
			size_hint: None, None
			width: 400
			height: 400
			pos_hint: {'center_x':.25, 'center_y': .6}
			nocache: True

		Button:
			id: run_btn
			text: "RUN"
			background_normal: ''
			background_color: rgba("#00ab66")
			color:0,0,0,1
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .19, "center_y": 0.2}
		
		Button:
			id: emergency
			text: "EM-STOP"
			background_normal: ''
			background_color: rgba("#ff0a01")
			color:0,0,0,1
			halign: "center"
			# background_color: get_color_from_hex('#FF0A01')
			# background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .35, "center_y": 0.2}
			on_press: app.emergency_stop()

		FloatLayout:
			#pos_hint: {"right": 1}
			# size_hint: 0.5, 0.5
			GridLayout:
				pos_hint: {"center_x": 0.5, "center_y": 0.4}
				col_default_width: '56dp'
				size_hint_x: None
				cols: 8
				row_default_height: '32dp'
				size_hint_y: None
				height: self.minimum_height
				Label:
					bold: True
					font_size: '10sp'
					text: 'SENSOR'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'ID'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'POS CTRL' 
					color: (0,0,0,1)		   
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL POS'  
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'CUR POS'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'VEL CTRL'
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL VEL' 
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'SEND'
					color: (0,0,0,1)
				# Motor 1
				CheckBox:
					id: m1_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m1_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '1'
					id: m1_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m1_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m1_command_callback()
					#size_hint:(None, .5)
					#width: 200
				TextInput:
					id: m1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m1_slider.value)
				Label:
					text: str(m1_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo1_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo1_slider.value)
				Button:
					id: pub1
					text: 'Pub'
					on_press:app.send_position(m1_id.text, m1_slider.value, velo1_slider.value, "pub1")
				# Motor 2
				CheckBox:
					id: m2_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m2_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '3'
					id: m2_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m2_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m2_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m2_slider.value)
				Label:
					text: str(m2_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo2_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo2_slider.value)
				Button:
					id: pub2
					text: 'Pub'
					on_press:app.send_position(m2_id.text, m2_slider.value, velo2_slider.value, "pub2")

				# Motor 3
				CheckBox:
					id: m3_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m3_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '5'
					id: m3_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m3_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m3_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m3_slider.value)
				Label:
					text: str(m3_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo3_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo3_slider.value)
				Button:
					id: pub3
					text: 'Pub'
					on_press:app.send_position(m3_id.text, m3_slider.value, velo3_slider.value, "pub3")

				# Motor 4
				CheckBox:
					id: m4_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m4_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '7'
					id: m4_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m4_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m4_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m4_slider.value)
				Label:
					text: str(m4_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo4_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo4_slider.value)
				Button:
					id: pub4
					text: 'Pub'
					on_press:app.send_position(m4_id.text, m4_slider.value, velo4_slider.value, "pub4")

				# Motor 5
				CheckBox:
					id: m5_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m5_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '9'
					id: m5_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m5_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m5_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m5_slider.value)
				Label:
					text: str(m5_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo5_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo5_slider.value)
				Button:
					id: pub5
					text: 'Pub'
					on_press:app.send_position(m5_id.text, m5_slider.value, velo5_slider.value, "pub5")

				# Motor 6
				CheckBox:
					id: m6_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m6_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '11'
					id: m6_id
					color: (0,0,1,1)
					size_hint_x: .40
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m6_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m6_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m6_slider.value)
				Label:
					text: str(m6_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo6_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo6_slider.value)
				Button:
					id: pub6
					text: 'Pub'
					on_press:app.send_position(m6_id.text, m6_slider.value, velo6_slider.value, "pub6")

				# Motor 7
				CheckBox:
					id: m7_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m7_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '13'
					id: m7_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m7_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m7_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m7_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m7_slider.value)
				Label:
					text: str(m7_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo7_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo7_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo7_slider.value)
				Button:
					id: pub7
					text: 'Pub'
					on_press:app.send_position(m7_id.text, m7_slider.value, velo7_slider.value, "pub7")
				
				#hand motors
				CheckBox:
					id: m8_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m8_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '31'
					id: m8_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
							
				Slider:
					id: m8_slider
					value: 0
					min: 0
					max: 5
					step: 1
					on_touch_up: root.m8_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m8_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m8_slider.value)
				Label:
					text: str(m8_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo8_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo8_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo8_slider.value)
				Button:
					id: pub8
					text: 'Pub'
					on_press:app.send_position(m8_id.text, m8_slider.value, velo8_slider.value, "pub8")
				

				CheckBox:
					id: m9_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m9_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '33'
					id: m9_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m9_slider
					value: 0
					min: 0
					max: 5
					step: 1
					on_touch_up: root.m9_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m9_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m9_slider.value)
				Label:
					text: str(m9_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo9_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo9_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo9_slider.value)
				Button:
					id: pub9
					text: 'Pub'
					on_press:app.send_position(m9_id.text, m9_slider.value, velo9_slider.value, "pub9")


				CheckBox:
					id: m10_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m10_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '35'
					id: m10_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m10_slider
					value: 0
					min: 0
					max: 5
					step: 1
					on_touch_up: root.m10_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m10_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m10_slider.value)
				Label:
					text: str(m10_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo10_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo10_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo10_slider.value)
				Button:
					id: pub10
					text: 'Pub'
					on_press:app.send_position(m10_id.text, m10_slider.value, velo10_slider.value, "pub10")
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				icon: 'cog'

<MenuHeadScreen>:
	name: 'home_head_control'
	img: h_asyn_image
	m1_pos_slider: m1_slider 
	m2_pos_slider: m2_slider 

	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "[b]Humanoid Control Panel[/b]"
			anchor_title: "center"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["engine", lambda x: app.callback(x)], ["robot-confused-outline", lambda x: app.set_screen('id')], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		AsyncImage:
			id: h_asyn_image
			source: root.image_path
			size_hint: None, None
			width: 400
			height: 400
			pos_hint: {'center_x':.25, 'center_y': .6}
			nocache: True

		Button:
			id: run_btn
			text: "RUN"
			background_normal: ''
			background_color: rgba("#00ab66")
			color:0,0,0,1
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .19, "center_y": 0.2}
		
		Button:
			id: emergency
			text: "EM-STOP"
			background_normal: ''
			background_color: rgba("#ff0a01")
			color:0,0,0,1
			halign: "center"
			# background_color: get_color_from_hex('#FF0A01')
			# background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .35, "center_y": 0.2}
			on_press: app.emergency_stop()

		FloatLayout:
			#pos_hint: {"right": 1}
			# size_hint: 0.5, 0.5
			GridLayout:
				pos_hint: {"center_x": 0.5, "center_y": 0.4}
				col_default_width: '56dp'
				size_hint_x: None
				cols: 8
				row_default_height: '32dp'
				size_hint_y: None
				height: self.minimum_height
				Label:
					bold: True
					font_size: '10sp'
					text: 'SENSOR'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'ID'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'POS CTRL' 
					color: (0,0,0,1)			  
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL POS'  
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'CUR POS'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'VEL CTRL'
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL VEL' 
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'SEND'
					color: (0,0,0,1)
				# Motor 1
				CheckBox:
					id: m1_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m1_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '41'
					id: m1_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m1_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m1_command_callback()
					#size_hint:(None, .5)
					#width: 200
				TextInput:
					id: m1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m1_slider.value)
				Label:
					text: str(m1_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo1_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo1_slider.value)
				Button:
					id: pub1
					text: 'Pub'
					on_press:app.send_position(m1_id.text, m1_slider.value, velo1_slider.value, "pub1")
				# Motor 2
				CheckBox:
					id: m2_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m2_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '42'
					id: m2_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m2_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m2_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m2_slider.value)
				Label:
					text: str(m2_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo2_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo2_slider.value)	
				Button:
					id: pub2
					text: 'Pub'
					on_press:app.send_position(m2_id.text, m2_slider.value, velo2_slider.value, "pub2")
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				icon: 'cog'

<MenuTorsoScreen>:
	name: 'home_torso_control'
	img: t_asyn_image
	m1_pos_slider: m1_slider
	m2_pos_slider: m2_slider
	m3_pos_slider: m3_slider

	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "[b]Humanoid Control Panel[/b]"
			anchor_title: "center"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["engine", lambda x: app.callback(x)], ["robot-confused-outline", lambda x: app.set_screen('id')], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		AsyncImage:
			id: t_asyn_image
			source: root.image_path
			size_hint: None, None
			width: 400
			height: 400
			pos_hint: {'center_x':.25, 'center_y': .6}
			nocache: True

		Button:
			id: run_btn
			text: "RUN"
			background_normal: ''
			background_color: rgba("#00ab66")
			color:0,0,0,1
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .19, "center_y": 0.2}
		
		Button:
			id: emergency
			text: "EM-STOP"
			background_normal: ''
			background_color: rgba("#ff0a01")
			color:0,0,0,1
			halign: "center"
			# background_color: get_color_from_hex('#FF0A01')
			# background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .35, "center_y": 0.2}
			on_press: app.emergency_stop()

		FloatLayout:
			#pos_hint: {"right": 1}
			# size_hint: 0.5, 0.5
			GridLayout:
				pos_hint: {"center_x": 0.5, "center_y": 0.4}
				col_default_width: '56dp'
				size_hint_x: None
				cols: 8
				row_default_height: '32dp'
				size_hint_y: None
				height: self.minimum_height
				Label:
					bold: True
					font_size: '10sp'
					text: 'SENSOR'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'ID'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'POS CTRL' 
					color: (0,0,0,1)			  
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL POS'  
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'CUR POS'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'VEL CTRL'
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL VEL' 
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'SEND'
					color: (0,0,0,1)
				# Motor 1
				CheckBox:
					id: m1_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m1_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '27'
					id: m1_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m1_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m1_command_callback()
					#size_hint:(None, .5)
					#width: 200
				TextInput:
					id: m1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m1_slider.value)
				Label:
					text: str(m1_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo1_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo1_slider.value) 
				Button:
					id: pub1
					text: 'Pub'
					on_press:app.send_position(m1_id.text, m1_slider.value, velo1_slider.value, "pub1")
				# Motor 2
				CheckBox:
					id: m2_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m2_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '28'
					id: m2_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m2_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m2_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m2_slider.value)
				Label:
					text: str(m2_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo2_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo2_slider.value) 
				Button:
					id: pub2
					text: 'Pub'
					on_press:app.send_position(m2_id.text, m2_slider.value, velo2_slider.value, "pub2")

				# Motor 3
				CheckBox:
					id: m3_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m3_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '29'
					id: m3_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m3_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m3_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m3_slider.value)
				Label:
					text: str(m3_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo3_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo3_slider.value) 
				Button:
					id: pub3
					text: 'Pub'
					on_press:app.send_position(m3_id.text, m3_slider.value, velo3_slider.value, "pub3")
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				icon: 'cog'

<MenuLeftLegScreen>:
	name: 'home_leftleg_control'
	img: ll_asyn_image
	m1_pos_slider: m1_slider
	m2_pos_slider: m2_slider
	m3_pos_slider: m3_slider
	m4_pos_slider: m4_slider
	m5_pos_slider: m5_slider
	m6_pos_slider: m6_slider

	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "[b]Humanoid Control Panel[/b]"
			anchor_title: "center"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["engine", lambda x: app.callback(x)], ["robot-confused-outline", lambda x: app.set_screen('id')], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		AsyncImage:
			id: ll_asyn_image
			source: root.image_path
			size_hint: None, None
			width: 400
			height: 400
			pos_hint: {'center_x':.25, 'center_y': .6}
			nocache: True

		Button:
			id: run_btn
			text: "RUN"
			background_normal: ''
			background_color: rgba("#00ab66")
			color:0,0,0,1
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .19, "center_y": 0.2}
		
		Button:
			id: emergency
			text: "EM-STOP"
			background_normal: ''
			background_color: rgba("#ff0a01")
			color:0,0,0,1
			halign: "center"
			# background_color: get_color_from_hex('#FF0A01')
			# background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .35, "center_y": 0.2}
			on_press: app.emergency_stop()

		FloatLayout:
			#pos_hint: {"right": 1}
			# size_hint: 0.5, 0.5
			GridLayout:
				pos_hint: {"center_x": 0.5, "center_y": 0.4}
				col_default_width: '56dp'
				size_hint_x: None
				cols: 8
				row_default_height: '32dp'
				size_hint_y: None
				height: self.minimum_height
				Label:
					bold: True
					font_size: '10sp'
					text: 'SENSOR'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'ID'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'POS CTRL' 
					color: (0,0,0,1)			  
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL POS'  
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'CUR POS'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'VEL CTRL'
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL VEL' 
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'SEND'
					color: (0,0,0,1)
				# Motor 1
				CheckBox:
					id: m1_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m1_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '16'
					id: m1_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m1_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m1_command_callback()
					#size_hint:(None, .5)
					#width: 200
				TextInput:
					id: m1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m1_slider.value)
				Label:
					text: str(m1_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo1_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo1_slider.value) 
				Button:
					id: pub1
					text: 'Pub'
					on_press:app.send_position(m1_id.text, m1_slider.value, velo1_slider.value, "pub1")
					disable: False

				# Motor 2
				CheckBox:
					id: m2_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m2_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '18'
					id: m2_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m2_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m2_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m2_slider.value)
				Label:
					text: str(m2_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo2_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo2_slider.value) 
				Button:
					id: pub2
					text: 'Pub'
					on_press:app.send_position(m2_id.text, m2_slider.value, velo2_slider.value, "pub2")

				# Motor 3
				CheckBox:
					id: m3_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m3_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '20'
					id: m3_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m3_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m3_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m3_slider.value)
				Label:
					text: str(m3_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo3_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo3_slider.value) 
				Button:
					id: pub3
					text: 'Pub'
					on_press:app.send_position(m3_id.text, m3_slider.value, velo3_slider.value, "pub3")

				# Motor 4
				CheckBox:
					id: m4_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m4_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '22'
					id: m4_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m4_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m4_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m4_slider.value)
				Label:
					text: str(m4_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo4_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo4_slider.value) 
				Button:
					id: pub4
					text: 'Pub'
					on_press:app.send_position(m4_id.text, m4_slider.value, velo4_slider.value, "pub4")

				# Motor 5
				CheckBox:
					id: m5_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m5_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '24'
					id: m5_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m5_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m5_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m5_slider.value)
				Label:
					text: str(m5_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo5_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo5_slider.value) 
				Button:
					id: pub5
					text: 'Pub'
					on_press:app.send_position(m5_id.text, m5_slider.value, velo5_slider.value, "pub5")

				# Motor 6
				CheckBox:
					id: m6_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m6_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '26'
					id: m6_id
					color: (0,0,1,1)
					size_hint_x: .40
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m6_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m6_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m6_slider.value)
				Label:
					text: str(m6_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo6_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo6_slider.value) 
				Button:
					id: pub6
					text: 'Pub'
					on_press:app.send_position(m6_id.text, m6_slider.value, velo6_slider.value, "pub6")
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				icon: 'cog'

<MenuRightLegScreen>:
	name: 'home_rightleg_control'
	img: rl_asyn_image
	m1_pos_slider: m1_slider
	m2_pos_slider: m2_slider
	m3_pos_slider: m3_slider
	m4_pos_slider: m4_slider
	m5_pos_slider: m5_slider
	m6_pos_slider: m6_slider

	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "[b]Humanoid Control Panel[/b]"
			anchor_title: "center"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["engine", lambda x: app.callback(x)], ["robot-confused-outline", lambda x: app.set_screen('id')], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		AsyncImage:
			id: rl_asyn_image
			source: root.image_path
			size_hint: None, None
			width: 400
			height: 400
			pos_hint: {'center_x':.25, 'center_y': .6}
			nocache: True

		Button:
			id: run_btn
			text: "RUN"
			background_normal: ''
			background_color: rgba("#00ab66")
			color:0,0,0,1
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .19, "center_y": 0.2}
		
		Button:
			id: emergency
			text: "EM-STOP"
			background_normal: ''
			background_color: rgba("#ff0a01")
			color:0,0,0,1
			halign: "center"
			# background_color: get_color_from_hex('#FF0A01')
			# background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .35, "center_y": 0.2}
			on_press: app.emergency_stop()

		FloatLayout:
			#pos_hint: {"right": 1}
			# size_hint: 0.5, 0.5
			GridLayout:
				pos_hint: {"center_x": 0.5, "center_y": 0.4}
				col_default_width: '56dp'
				size_hint_x: None
				cols: 8
				row_default_height: '32dp'
				size_hint_y: None
				height: self.minimum_height
				Label:
					bold: True
					font_size: '10sp'
					text: 'SENSOR'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'ID'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'POS CTRL' 
					color: (0,0,0,1)			  
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL POS'  
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'CUR POS'
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'VEL CTRL'
					color: (0,0,0,1) 
				Label:
					bold: True
					font_size: '10sp'
					text: 'GOAL VEL' 
					color: (0,0,0,1)
				Label:
					bold: True
					font_size: '10sp'
					text: 'SEND'
					color: (0,0,0,1)
				# Motor 1
				CheckBox:
					id: m1_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m1_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '15'
					id: m1_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m1_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m1_command_callback()
					#size_hint:(None, .5)
					#width: 200
				TextInput:
					id: m1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m1_slider.value)
				Label:
					text: str(m1_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo1_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo1_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo1_slider.value) 
				Button:
					id: pub1
					text: 'Pub'
					on_press:app.send_position(m1_id.text, m1_slider.value, velo1_slider.value, "pub1")
					disable: False
				# Motor 2
				CheckBox:
					id: m2_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m2_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '17'
					id: m2_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m2_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m2_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m2_slider.value)
				Label:
					text: str(m2_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo2_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo2_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo2_slider.value) 
				Button:
					id: pub2
					text: 'Pub'
					on_press:app.send_position(m2_id.text, m2_slider.value, velo2_slider.value, "pub2")

				# Motor 3
				CheckBox:
					id: m3_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m3_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '19'
					id: m3_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m3_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m3_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m3_slider.value)
				Label:
					text: str(m3_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo3_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo3_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo3_slider.value) 
				Button:
					id: pub3
					text: 'Pub'
					on_press:app.send_position(m3_id.text, m3_slider.value, velo3_slider.value, "pub3")

				# Motor 4
				CheckBox:
					id: m4_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m4_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '21'
					id: m4_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m4_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m4_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m4_slider.value)
				Label:
					text: str(m4_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo4_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo4_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo4_slider.value) 
				Button:
					id: pub4
					text: 'Pub'
					on_press:app.send_position(m4_id.text, m4_slider.value, velo4_slider.value, "pub4")

				# Motor 5
				CheckBox:
					id: m5_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m5_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '23'
					id: m5_id
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m5_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m5_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m5_slider.value)
				Label:
					text: str(m5_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo5_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo5_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo5_slider.value) 
				Button:
					id: pub5
					text: 'Pub'
					on_press:app.send_position(m5_id.text, m5_slider.value, velo5_slider.value, "pub5")

				# Motor 6
				CheckBox:
					id: m6_checkbox
					group: "checkboxes"
					color: 1, 1, 1, 1
					on_active: app.test(m6_id.text)
					size_hint_x: .20
					canvas.before:
						Color:
							rgb: 1,0,0
						Ellipse:
							pos:self.center_x-8, self.center_y-8
							size:[16,16]
						Color:
							rgb: 0,0,0
						Ellipse:
							pos:self.center_x-7, self.center_y-7
							size:[14,14]
				Label:
					text: '25'
					id: m6_id
					color: (0,0,1,1)
					size_hint_x: .40
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: m6_slider
					value: 0
					min: -180
					max: 180
					step: 1
					on_touch_up: root.m6_command_callback()
					#size_hint:(None, .5)sectiition(m2_id.text, m2_slider.value)
				TextInput:
					id: m6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(m6_slider.value)
				Label:
					text: str(m6_slider.value)
					color: (0,0,1,1)
					canvas.before:
						Color:
							rgba: 1, 1, 1, 1
						Rectangle:
							pos: self.pos
							size: self.size
				Slider:
					id: velo6_slider
					value: 750
					min: 1
					max: 1500
					step: 1
					#size_hint:(None, .5)
					#width: 200	
				TextInput:
					id: velo6_textinput
					# size_hint_x: None
					# width: 30
					input_filter: 'int'
					multiline: False
					text: str(velo6_slider.value) 
				Button:
					id: pub6
					text: 'Pub'
					on_press:app.send_position(m6_id.text, m6_slider.value, velo6_slider.value, "pub6")
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				icon: 'cog'

<IDScreen>:
	name: 'id'
	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "Humanoid Control Panel"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["robot-confused-outline", lambda x: app.callback_1()], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}

		# Image
		AsyncImage:
			source: 'robot_map.jpg'
			size_hint: 1, 1
			size_hint: None, None
			width: 625
			height: 625
			pos_hint: {'center_x':.50, 'center_y': .50}
		
		MDTabs:
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.01}
	
<LIDARScreen>:
	name: 'lidar'
	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "LIDAR Panel"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["robot-confused-outline", lambda x: app.callback_1()], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
		
		Button:
			id: lidar_stream
			text: "Visualise Lidar readings"
			background_color: 0,0,1,1	  
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .5, "center_y": 0.55}
			on_press: root.run_lidar_thread()
		
		MDLabel:
			text: "Lidar : Velodyne VLP-16"
			pos_hint: {"center_x": 0.9, "center_y": 0.45}
		
		MDLabel:
			text: "Resolution : 0.1 degrees"
			pos_hint: {"center_x": 0.9, "center_y": 0.40}
		
		MDLabel:
			text: "Lidar Motor speed : 600RPM"
			pos_hint: {"center_x": 0.875, "center_y": 0.35}
  
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				text: 'lidar'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				text: 'realsense'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				text: 'imu'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				text: 'ft'
				icon: 'cog'

<RealsenseScreen>:
	name: 'realsense'
	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "Realsense Panel"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["robot-confused-outline", lambda x: app.callback_1()], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}

		Button:
			id: cam 
			text: "Connect T265 Camera "
			background_color: 0,0,1,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .5, "center_y": 0.75}
				  
		Button:
			id: cam_live_stream 
			text: "View Live stream "
			background_color: 0,1,0,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .5, "center_y": 0.55}
			
		Button:
			id: emergency
			text: "EM-STOP"
			halign: "center"
			background_color: get_color_from_hex('#FF0A01')
			#background_color: 0,1,0,1
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .5, "center_y": 0.35}
			on_press: app.emergency_stop()
  
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				text: 'lidar'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				text: 'realsense'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				text: 'imu'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				text: 'ft'
				icon: 'cog'

<IMUScreen>:
	name: 'imu'
	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "IMU Panel"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["robot-confused-outline", lambda x: app.callback_1()], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
  
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				text: 'lidar'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				text: 'realsense'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				text: 'imu'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				text: 'ft'
				icon: 'cog'
		
		Button:
			id: imu 
			text: "Connect VectorNav IMU "
			background_color: 0,0,1,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .5125, "center_y": 0.77}
			on_press: root.init_imu()
		
		MDLabel:
			text: "Orientation"
			pos_hint: {"center_x": 0.75, "center_y": 0.6}
			bold: True
		
		MDLabel:
			text: "Angular Velocity"
			pos_hint: {"center_x": 0.925, "center_y": 0.6}
			bold: True
		MDLabel:
			text: "Linear Accelertion"
			pos_hint: {"center_x": 1.125, "center_y": 0.6}
			bold: True
		MDLabel:
			text: "Roll :"
			pos_hint: {"center_x": 0.75, "center_y": 0.55}
			bold: True
		MDLabel:
			text: root.data_label_imu_x
			pos_hint: {"center_x": 0.8, "center_y": 0.55}
		MDLabel:
			text: "Pitch :"
			pos_hint: {"center_x": 0.75, "center_y": 0.5}
			bold: True
		MDLabel:
			text: root.data_label_imu_y
			pos_hint: {"center_x": 0.8, "center_y": 0.5}
		MDLabel:
			text: "Yaw :"
			pos_hint: {"center_x": 0.75, "center_y": 0.45}
			bold: True
		MDLabel:
			text: root.data_label_imu_z
			pos_hint: {"center_x": 0.8, "center_y": 0.45}
		MDLabel:
			text: "X:"
			pos_hint: {"center_x": 0.925, "center_y": 0.55}
			bold: True
		MDLabel:
			text: root.data_label_ang_vel_x
			pos_hint: {"center_x": 0.975, "center_y": 0.55}
		MDLabel:
			text: "Y:"
			pos_hint: {"center_x": 0.925, "center_y": 0.5}
			bold: True
		MDLabel:
			text: root.data_label_ang_vel_y
			pos_hint: {"center_x": 0.975, "center_y": 0.5}
		MDLabel:
			text: "Z:"
			pos_hint: {"center_x": 0.925, "center_y": 0.45}
			bold: True
		MDLabel:
			text: root.data_label_ang_vel_z
			pos_hint: {"center_x": 0.975, "center_y": 0.45}
		MDLabel:
			text: "X:"
			pos_hint: {"center_x": 1.125, "center_y": 0.55}
			bold: True
		MDLabel:
			text: root.data_label_acc_x
			pos_hint: {"center_x": 1.175, "center_y": 0.55}
		MDLabel:
			text: "Y:"
			pos_hint: {"center_x": 1.125, "center_y": 0.5}
			bold: True
		MDLabel:
			text: root.data_label_acc_y
			pos_hint: {"center_x": 1.175, "center_y": 0.5}
		MDLabel:
			text: "Z:"
			pos_hint: {"center_x": 1.125, "center_y": 0.45}
			bold: True
		MDLabel:
			text: root.data_label_acc_z
			pos_hint: {"center_x": 1.175, "center_y": 0.45}
		Button:
			id: gps
			text: "Enable GPS "
			background_color: 0,0,1,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .5125, "center_y": 0.35}
			on_press: root.init_gps()
		MDLabel:
			text: "status:"
			pos_hint: {"center_x": 0.925, "center_y": 0.25}
			bold: True
		MDLabel:
			text: root.data_label_gps_status
			pos_hint: {"center_x": 1.025, "center_y": 0.25}
		MDLabel:
			text: "Latitude:"
			pos_hint: {"center_x": 0.925, "center_y": 0.2}
			bold: True
		MDLabel:
			text: root.data_label_lat
			pos_hint: {"center_x": 1.025, "center_y": 0.2}
		MDLabel:
			text: "Longitude:"
			pos_hint: {"center_x": 0.925, "center_y": 0.15}
			bold: True
		MDLabel:
			text: root.data_label_longi
			pos_hint: {"center_x": 1.025, "center_y": 0.15}	

<FTScreen>:
	name: 'ft'
	img: asyn_image
	FloatLayout:
		orientation: "vertical"

		MDTopAppBar:
			title: "Force-Torque Sensor Panel"
			left_action_items: [["home-analytics", lambda x: app.set_screen('home')]]
			right_action_items: [["robot-confused-outline", lambda x: app.callback_1()], ["power", lambda x: app.callback_2()]]
			size_hint: 1, .1
			pos_hint: {"center_x": .5, "center_y": 0.95}
			
		AsyncImage:
			id: asyn_image
			source: root.image_path
			size_hint: None, None
			width: 300
			height: 300
			pos_hint: {'center_x':.25, 'center_y': .6}
			nocache: True
		
		MDCheckbox:
			pos_hint: {"center_x": 0.9, "center_y": 0.67}
			size_hint: .1,.1
			on_active: root.r_wr_ft_sensor()
			
		MDCheckbox:
			pos_hint: {"center_x": 0.9, "center_y": 0.77}
			size_hint: .1,.1
			on_active: root.l_wr_ft_sensor()
			
		MDCheckbox:
			pos_hint: {"center_x": 0.9, "center_y": 0.57}
			size_hint: .1,.1
			on_active: root.l_leg_ft_sensor()
			
		MDCheckbox:
			pos_hint: {"center_x": 0.9, "center_y": 0.47}
			size_hint: .1,.1
			on_active: root.r_leg_ft_sensor()
		
		MDCheckbox:
			group: "values"
			pos_hint: {"center_x": 0.8, "center_y": 0.67}
			size_hint: .1,.1
			on_active: root.rw_checkbox(*args)
			
		MDCheckbox:
			group : "values"
			pos_hint: {"center_x": 0.8, "center_y": 0.77}
			size_hint: .1,.1
			on_active: root.lw_checkbox(*args)
			
		MDCheckbox:
			group: "values"
			pos_hint: {"center_x": 0.8, "center_y": 0.57}
			size_hint: .1,.1
			on_active: root.ll_checkbox(*args)
			
		MDCheckbox:
			group: "values"
			pos_hint: {"center_x": 0.8, "center_y": 0.47}
			size_hint: .1,.1
			on_active: root.rl_checkbox(*args)
		
		Button:
			id: fts1 
			text: "connect l_wr_ft_sensor"
			background_color: 0,1,1,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .58, "center_y": 0.77}
			#on_press: root.init_force_node()
		
		Button:
			id: fts2
			text: "connect r_wr_ft_sensor"
			background_color: 1,0,0,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .58, "center_y": 0.67}
		
		Button:
			id: fts3
			text: "connect l_an_ft_sensor"
			background_color: 0,0,1,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .58, "center_y": 0.57}
		
		Button:
			id: fts4 
			text: "connect r_an_ft_sensor"
			background_color: 0,1,0,1
			halign: "center"
			size_hint: 0.25, 0.1
			pos_hint: {"center_x": .58, "center_y": 0.47}
			
		MDLabel:
			text: "Values"
			pos_hint: {"center_x": 1.27, "center_y": 0.82}
				
		MDLabel:
			text: "Vector"
			pos_hint: {"center_x": 1.37, "center_y": 0.82}
		
		MDLabel:
			text: "Forces:"
			pos_hint: {"center_x": 1.1, "center_y": 0.38}
			
		MDLabel:
			text: "X:"
			pos_hint: {"center_x": 1.15, "center_y": 0.35}
		
		MDLabel:
			text: "Y:"
			pos_hint: {"center_x": 1.15, "center_y": 0.32}
		
		MDLabel:
			text: "Z:"
			pos_hint: {"center_x": 1.15, "center_y": 0.29}
		
		MDLabel:
			text: "Torque:"
			pos_hint: {"center_x": 1.1, "center_y": 0.23}
			
		MDLabel:
			text: "X:"
			pos_hint: {"center_x": 1.15, "center_y": 0.20}
		
		MDLabel:
			text: "Y:"
			pos_hint: {"center_x": 1.15, "center_y": 0.17}
		
		MDLabel:
			text: "Z:"
			pos_hint: {"center_x": 1.15, "center_y": 0.14}
		
		MDLabel:
			text: root.data_label_fx
			pos_hint: {"center_x": 1.18, "center_y": 0.35}
		
		MDLabel:
			text: root.data_label_fy
			pos_hint: {"center_x": 1.18, "center_y": 0.32}
		
		MDLabel:
			text: root.data_label_fz
			pos_hint: {"center_x": 1.18, "center_y": 0.29}
		
		MDLabel:
			text: root.data_label_tx
			pos_hint: {"center_x": 1.18, "center_y": 0.20}
		
		MDLabel:
			text: root.data_label_ty
			pos_hint: {"center_x": 1.18, "center_y": 0.17}
		
		MDLabel:
			text: root.data_label_tz
			pos_hint: {"center_x": 1.18, "center_y": 0.14}
			
		
		Button:
			id: refresh_btn
			text: "Refresh"
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .15, "center_y": 0.3}
			on_press: root.change_image("new_robotImage.png")
		
		Button:
			id: live_stream
			text: "Live Stream"
			halign: "center"
			size_hint: 0.15, 0.1
			pos_hint: {"center_x": .35, "center_y": 0.3}
			on_press: root.run_image_thread()
			
		Button:
			id: start_visu
			text: "Start Visualisation"
			halign: "center"
			size_hint: 0.2, 0.1
			pos_hint: {"center_x": .25, "center_y": 0.15}
			on_press: root.run_visu_thread()
			
		MDTabs:
			text_color_active: [0, 0, 0, 1]
			size_hint: 1, 0.08
			tab_hint_x: True
			allow_stretch: True
			on_tab_switch: app.on_tab_switch(*args)
			Tab:
				title: '[b]LiDAR[/b]'
				text: 'lidar'
				icon: 'motion-sensor'
			Tab:
				title: '[b]RealSense[/b]'
				text: 'realsense'
				icon: 'camera-outline'
			Tab:
				title: '[b]IMU[/b]'
				text: 'imu'
				icon: 'chart-waterfall'
			Tab:
				title: '[b]Force Torque[/b]'
				text: 'ft'
				icon: 'cog'
"""

class RobotJointState():
	joint_state = JointState()

	def __init__(self, **kwargs):
		self.joint_state.name.append('r_arm_sh_p1')
		self.joint_state.name.append('r_arm_sh_r')
		self.joint_state.name.append('r_arm_sh_p2')
		self.joint_state.name.append('r_arm_el_y')
		self.joint_state.name.append('r_arm_wr_r')
		self.joint_state.name.append('r_arm_wr_y')
		self.joint_state.name.append('r_arm_wr_p')
		self.joint_state.name.append('r_arm_grip_thumb')
		self.joint_state.name.append('r_arm_grip_index')
		self.joint_state.name.append('r_arm_grip_middle')

		self.joint_state.name.append('l_arm_sh_p1')
		self.joint_state.name.append('l_arm_sh_r')
		self.joint_state.name.append('l_arm_sh_p2')
		self.joint_state.name.append('l_arm_el_y')
		self.joint_state.name.append('l_arm_wr_r')
		self.joint_state.name.append('l_arm_wr_y')
		self.joint_state.name.append('l_arm_wr_p')
		self.joint_state.name.append('l_arm_grip_thumb')
		self.joint_state.name.append('l_arm_grip_index')
		self.joint_state.name.append('l_arm_grip_middle')
		
		self.joint_state.name.append('head_y')
		self.joint_state.name.append('head_p')
		self.joint_state.name.append('r_antenna')
		self.joint_state.name.append('l_antenna')
		self.joint_state.name.append('torso_y')

		self.joint_state.name.append('r_leg_hip_r')
		self.joint_state.name.append('r_leg_hip_y')
		self.joint_state.name.append('r_leg_hip_p')
		self.joint_state.name.append('r_leg_kn_p')
		self.joint_state.name.append('r_leg_an_p')
		self.joint_state.name.append('r_leg_an_r')
		self.joint_state.name.append('l_leg_hip_r')
		self.joint_state.name.append('l_leg_hip_y')
		self.joint_state.name.append('l_leg_hip_p')
		self.joint_state.name.append('l_leg_kn_p')
		self.joint_state.name.append('l_leg_an_p')
		self.joint_state.name.append('l_leg_an_r')

		for x in range(37):
			self.joint_state.position.append(0.0)

		self.joint_state.velocity = []
		self.joint_state.effort = []

	def copy(self, msg):
		self.joint_state.name = msg.name
		for x in range(37):
			self.joint_state.position[x] = msg.position[x]
		self.joint_state.velocity = msg.velocity
		self.joint_state.effort = msg.effort
		self.joint_state.header = msg.header
	
	def set_pos(self, id, val):
		self.joint_state.position[id] = val


#pub for joint state publisher
joint_pub = rospy.Publisher("joint_states", JointState, queue_size=10)
											
#kill rviz joint state publisher node
#os.system("rosnode kill /joint_state_publisher")

class Tab(MDFloatLayout, MDTabsBase):
	pass


class MenuScreen(Screen):
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	pass

	def __init__(self, **kwargs):
		super(MenuScreen, self).__init__(**kwargs)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()
	pass


class LIDARScreen(Screen):
	def run_lidar_view(self):
		command = "roslaunch velodyne_pointcloud VLP16_points.launch"
		subprocess.run(command, shell=True)
		
	def run_lidar_thread(self):
		lidar_thread = threading.Thread(target = self.run_lidar_view)
		lidar_thread.start()

class RealsenseScreen(Screen):
	pass

class IMUScreen(Screen):
	imu_x = 0
	imu_y = 0
	imu_z = 0
	imu_w = 0
	ang_vel_x = 0
	ang_vel_y = 0
	ang_vel_z = 0
	acc_x = 0
	acc_y = 0
	acc_z = 0
	gps_status = -1
	lat = 0
	longi = 0
	data_label_imu_x = StringProperty("NA")
	data_label_imu_y = StringProperty("NA")
	data_label_imu_z = StringProperty("NA")
	data_label_ang_vel_x = StringProperty("NA")
	data_label_ang_vel_y = StringProperty("NA")
	data_label_ang_vel_z = StringProperty("NA")
	data_label_acc_x = StringProperty("NA")
	data_label_acc_y = StringProperty("NA")
	data_label_acc_z = StringProperty("NA")
	data_label_gps_status = StringProperty("NA")
	data_label_lat = StringProperty("NA")
	data_label_longi = StringProperty("NA")
	
	def init_imu(self):
		print("Subscribing to IMU")
		subscriber = rospy.Subscriber("/vectornav/IMU", Imu, self.imu_callback)
		
	def init_gps(self):
		print("Subscribing to GPS")
		subscriber_gps = rospy.Subscriber("/vectornav/GPS", NavSatFix, self.gps_callback)
		 
	def imu_callback(self, msg):
			self.imu_x = round(msg.orientation.x,4)
			self.imu_y = round(msg.orientation.y,4)
			self.imu_z = round(msg.orientation.z,4)
			self.imu_w = round(msg.orientation.w,4)
			
			self.ang_vel_x = round(msg.angular_velocity.x,4)
			self.ang_vel_y = round(msg.angular_velocity.y,4)
			self.ang_vel_z = round(msg.angular_velocity.z,4)

			self.acc_x = round(msg.linear_acceleration.x,4)
			self.acc_y = round(msg.linear_acceleration.y,4)
			self.acc_z = round(msg.linear_acceleration.z,4)
			
			self.data_label_imu_x = str(self.imu_x)
			self.data_label_imu_y = str(self.imu_y)
			self.data_label_imu_z = str(self.imu_z)
			
			self.data_label_ang_vel_x = str(self.ang_vel_x)
			self.data_label_ang_vel_y = str(self.ang_vel_y)
			self.data_label_ang_vel_z = str(self.ang_vel_z)
			
			self.data_label_acc_x = str(self.acc_x)
			self.data_label_acc_y = str(self.acc_y)
			self.data_label_acc_z = str(self.acc_z)


			#print(f"orientaion : {self.imu_x},{self.imu_y},{self.imu_z},{self.imu_w}")
	def gps_callback(self,msg):
		#print(msg)
		self.gps_status = msg.status.status
		self.lat = msg.latitude
		self.longi = msg.longitude
		
		print(msg.status.status,msg.latitude,msg.longitude)
		
		if(self.gps_status != -1):
			self.data_label_gps_status =str(self.gps_status)
			self.data_label_lat = str(self.lat)
			self.data_label_longi = str(self.longi)
		else:
			self.data_label_gps_status =str(self.gps_status)
			self.data_label_lat = str("Satellite fix not achieved")
			self.data_label_longi = str("Satellite fix not achieved")
	

class FTScreen(Screen):
	
	#bringing the robot image here in the force torque screen
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	pass

	#def __init__(self, **kwargs):
		#super(MenuScreen, self).__init__(**kwargs)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()
	pass
	#*************************************************************************
	
	data_label_fz = StringProperty("Not connected")
	data_label_fy = StringProperty("Not connected")
	data_label_fx = StringProperty("Not connected")
	data_label_tz = StringProperty("Not connected")
	data_label_ty = StringProperty("Not connected")
	data_label_tx = StringProperty("Not connected")
	force_z = 0
	force_x = 0
	force_y = 0
	torque_z = 0
	torque_x = 0
	torque_y = 0
	def init_force_node(self):
		print("def init force node being executed")
		global visualising_ft_sensors, subscriber, create_node,subscribed_to_some_topic
		if(create_node == 0):
			#rospy.init_node('read_forces_torque', anonymous=True)
			print("Created a ros node")
			create_node+=1
		if(visualising_ft_sensors[4]==1):
			if(subscribed_to_some_topic == 1):
				subscriber.unregister()
				print("Unsubscibing from a previous topic")
			print("Subscribed to left hand sensor")
			subscriber = rospy.Subscriber("/bus0/ft_sensor0/ft_sensor_readings/wrench", WrenchStamped, self.wrench_callback_lh)
			subscribed_to_some_topic = 1

		if(visualising_ft_sensors[4]==2):
			if(subscribed_to_some_topic == 1):
				subscriber.unregister()
				print("Unsubscibing from a previous topic")
			print("Subscribed to right hand sensor")
			subscriber = rospy.Subscriber("/bus1/ft_sensor1/ft_sensor_readings/wrench", WrenchStamped, self.wrench_callback_rh)
			subscribed_to_some_topic = 1

		if(visualising_ft_sensors[4]==3):
			if(subscribed_to_some_topic == 1):
				subscriber.unregister()
				print("Unsubscibing from a previous topic")
			print("Subscribed to left leg sensor")
			subscriber = rospy.Subscriber("/bus2/ft_sensor2/ft_sensor_readings/wrench", WrenchStamped, self.wrench_callback_ll)
			subscribed_to_some_topic = 1

		if(visualising_ft_sensors[4]==4):
			if(subscribed_to_some_topic == 1):
				subscriber.unregister()
				print("Unsubscibing from a previous topic")
			print("Subscribed to right leg sensor")
			subscriber = rospy.Subscriber("/bus3/ft_sensor3/ft_sensor_readings/wrench", WrenchStamped, self.wrench_callback_rl)
			subscribed_to_some_topic = 1
		
	def wrench_callback_lh(self, msg):
		#print("executing left hand sensor callback")
		self.force_z = msg.wrench.force.z
		self.force_x = msg.wrench.force.x
		self.force_y = msg.wrench.force.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.torque_z = msg.wrench.torque.z
		self.torque_x = msg.wrench.torque.x
		self.torque_y = msg.wrench.torque.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.data_label_tz = str(self.torque_z)
		self.data_label_ty = str(self.torque_y)
		self.data_label_tx = str(self.torque_x)
		
	def wrench_callback_rh(self, msg):
		#print("executing right hand sensor callback")
		self.force_z = msg.wrench.force.z
		self.force_x = msg.wrench.force.x
		self.force_y = msg.wrench.force.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.torque_z = msg.wrench.torque.z
		self.torque_x = msg.wrench.torque.x
		self.torque_y = msg.wrench.torque.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.data_label_tz = str(self.torque_z)
		self.data_label_ty = str(self.torque_y)
		self.data_label_tx = str(self.torque_x)

	def wrench_callback_ll(self, msg):
		#print("executing left leg sensor callback")
		self.force_z = msg.wrench.force.z
		self.force_x = msg.wrench.force.x
		self.force_y = msg.wrench.force.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.torque_z = msg.wrench.torque.z
		self.torque_x = msg.wrench.torque.x
		self.torque_y = msg.wrench.torque.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.data_label_tz = str(self.torque_z)
		self.data_label_ty = str(self.torque_y)
		self.data_label_tx = str(self.torque_x)

	def wrench_callback_rl(self, msg):
		#print("executing right leg sensor callback")
		self.force_z = msg.wrench.force.z
		self.force_x = msg.wrench.force.x
		self.force_y = msg.wrench.force.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.torque_z = msg.wrench.torque.z
		self.torque_x = msg.wrench.torque.x
		self.torque_y = msg.wrench.torque.y
		self.data_label_fz = str(self.force_z)
		self.data_label_fy = str(self.force_y)
		self.data_label_fx = str(self.force_x)
		self.data_label_tz = str(self.torque_z)
		self.data_label_ty = str(self.torque_y)
		self.data_label_tx = str(self.torque_x)
		
	def run_image_view(self):
		command = "rosrun image_view image_view image:=/rviz1/camera1/image"
		subprocess.run(command, shell=True)
		print("I have jumped out")
		
	def run_image_thread(self):
		im_thread = threading.Thread(target = self.run_image_view)
		im_thread.start()
		
	def run_visualisation(self):
		command = "rosrun urdf-rviz test_marker_4.py"
		subprocess.run(command, shell=True)
		print("I have jumped out")
		
	def run_visu_thread(self):
		visu_thread = threading.Thread(target = self.run_visualisation)
		visu_thread.start()
		
	def write_file(self):
		global visualising_ft_sensors
		with open("shared_variable.txt", "w") as file:
			file.write(str(visualising_ft_sensors))
			
	
	def l_wr_ft_sensor(self):
		global visualising_ft_sensors,lw
		if(lw%2==0):
			visualising_ft_sensors[0] = 1
		else:
			visualising_ft_sensors[0] = 0
		print(visualising_ft_sensors)
		lw = lw + 1
		self.write_file()
		
	def r_wr_ft_sensor(self):
		global visualising_ft_sensors,rw
		if(rw%2==0):
			visualising_ft_sensors[1] = 1
		else:
			visualising_ft_sensors[1] = 0
		print(visualising_ft_sensors)
		rw = rw + 1
		self.write_file()
		
	def l_leg_ft_sensor(self):
		global visualising_ft_sensors,ll
		if(ll%2==0):
			visualising_ft_sensors[2] = 1
		else:
			visualising_ft_sensors[2] = 0
		print(visualising_ft_sensors)
		ll = ll + 1
		self.write_file()
		
	def r_leg_ft_sensor(self):
		global visualising_ft_sensors,rl
		if(rl%2==0):
			visualising_ft_sensors[3] = 1
		else:
			visualising_ft_sensors[3] = 0
		print(visualising_ft_sensors)
		rl = rl + 1
		self.write_file()
	
	def lw_checkbox(self,checkbox,active):
		global visualising_ft_sensors,lwrb
		if(lwrb%2==0):
			visualising_ft_sensors[4] = 1
		else:
			visualising_ft_sensors[4] = 0
		lwrb = lwrb + 1
		self.init_force_node()
		self.write_file()
	
	def rw_checkbox(self,checkbox,active):
		global visualising_ft_sensors,rwrb
		if(rwrb%2==0):
			visualising_ft_sensors[4] = 2
		else:
			visualising_ft_sensors[4] = 0
		rwrb = rwrb + 1
		self.init_force_node()
		self.write_file()
	
	def ll_checkbox(self,checkbox,active):
		global visualising_ft_sensors,llrb
		if(llrb%2==0):
			visualising_ft_sensors[4] = 3
		else:
			visualising_ft_sensors[4] = 0
		llrb = llrb + 1
		self.init_force_node()
		self.write_file()
	
	def rl_checkbox(self,checkbox,active):
		global visualising_ft_sensors,rlrb
		if(rlrb%2==0):
			visualising_ft_sensors[4] = 4
		else:
			visualising_ft_sensors[4] = 0
		rlrb = rlrb + 1
		self.init_force_node()
		self.write_file()

class MenuScreen(Screen):
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	pass

	def __init__(self, **kwargs):
		super(MenuScreen, self).__init__(**kwargs)
		
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()

class MenuHeadScreen(Screen):
	#image info
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")

	rjs = RobotJointState()

	#r_antenna properties
	m1_pos_slider = ObjectProperty(None)

	#l_antenna properties
	m2_pos_slider = ObjectProperty(None)
	pass

	def __init__(self, **kwargs):
		super(MenuHeadScreen, self).__init__(**kwargs)
		self.command_sub = rospy.Subscriber("joint_states", JointState,
											self.update_rjs, queue_size=10)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()

	def update_rjs(self, msg):
		self.rjs.copy(msg)
		
	def m1_command_callback(self):
		self.rjs.joint_state.position[22] = self.m1_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m2_command_callback(self):
		self.rjs.joint_state.position[23] = self.m2_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

class MenuTorsoScreen(Screen):
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	
	rjs = RobotJointState()

	#torso_y properties
	m1_pos_slider = ObjectProperty(None)

	#head_y properties
	m2_pos_slider = ObjectProperty(None)

	#head_p properties
	m3_pos_slider = ObjectProperty(None)
	pass

	def __init__(self, **kwargs):
		super(MenuTorsoScreen, self).__init__(**kwargs)
		self.command_sub = rospy.Subscriber("joint_states", JointState,
											self.update_rjs, queue_size=10)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()

	def update_rjs(self, msg):
		self.rjs.copy(msg)
		
	def m1_command_callback(self):
		self.rjs.joint_state.position[24] = self.m1_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m2_command_callback(self):
		self.rjs.joint_state.position[20] = self.m2_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m3_command_callback(self):
		self.rjs.joint_state.position[21] = self.m3_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

class MenuLeftArmScreen(Screen):
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	
	rjs = RobotJointState()

	#l_arm_sh_p1 properties
	m1_pos_slider = ObjectProperty(None)

	#l_arm_sh_r properties
	m2_pos_slider = ObjectProperty(None)

	#l_arm_sh_p2 properties
	m3_pos_slider = ObjectProperty(None)

	#l_arm_el_y properties
	m4_pos_slider = ObjectProperty(None)

	#l_arm_wr_r properties
	m5_pos_slider = ObjectProperty(None)

	#l_arm_wr_y properties
	m6_pos_slider = ObjectProperty(None)

	#l_arm_wr_p properties
	m7_pos_slider = ObjectProperty(None)

	#l_arm_grip_thumb properties
	m8_pos_slider = ObjectProperty(None)

	#l_arm_grip_index properties
	m9_pos_slider = ObjectProperty(None)

	#l_arm_grip_middle properties
	m10_pos_slider = ObjectProperty(None)
	pass

	def __init__(self, **kwargs):
		super(MenuLeftArmScreen, self).__init__(**kwargs)
		self.command_sub = rospy.Subscriber("joint_states", JointState,
											self.update_rjs, queue_size=10)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()

	def update_rjs(self, msg):
		self.rjs.copy(msg)
		
	def m1_command_callback(self):
		self.rjs.joint_state.position[10] = self.m1_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m2_command_callback(self):
		self.rjs.joint_state.position[11] = self.m2_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m3_command_callback(self):
		self.rjs.joint_state.position[12] = self.m3_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m4_command_callback(self):
		self.rjs.joint_state.position[13] = self.m4_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m5_command_callback(self):
		self.rjs.joint_state.position[14] = self.m5_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m6_command_callback(self):
		self.rjs.joint_state.position[15] = self.m6_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m7_command_callback(self):
		self.rjs.joint_state.position[16] = self.m7_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m8_command_callback(self):
		self.rjs.joint_state.position[17] = self.m8_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m9_command_callback(self):
		self.rjs.joint_state.position[18] = self.m9_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m10_command_callback(self):
		self.rjs.joint_state.position[19] = self.m10_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

class MenuRightArmScreen(Screen):
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	
	rjs = RobotJointState()

	#r_arm_sh_p1 properties
	m1_pos_slider = ObjectProperty(None)

	#r_arm_sh_r properties
	m2_pos_slider = ObjectProperty(None)

	#r_arm_sh_p2 properties
	m3_pos_slider = ObjectProperty(None)

	#r_arm_el_y properties
	m4_pos_slider = ObjectProperty(None)

	#r_arm_wr_r properties
	m5_pos_slider = ObjectProperty(None)

	#r_arm_wr_y properties
	m6_pos_slider = ObjectProperty(None)

	#r_arm_wr_p properties
	m7_pos_slider = ObjectProperty(None)

	#r_arm_grip_thumb properties
	m8_pos_slider = ObjectProperty(None)

	#r_arm_grip_index properties
	m9_pos_slider = ObjectProperty(None)

	#r_arm_grip_middle properties
	m10_pos_slider = ObjectProperty(None)
	pass

	def __init__(self, **kwargs):
		super(MenuRightArmScreen, self).__init__(**kwargs)
		self.command_sub = rospy.Subscriber("joint_states", JointState,
											self.update_rjs, queue_size=10)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()
	
	def update_rjs(self, msg):
		self.rjs.copy(msg)
		
	def m1_command_callback(self):
		self.rjs.joint_state.position[0] = self.m1_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m2_command_callback(self):
		self.rjs.joint_state.position[1] = self.m2_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m3_command_callback(self):
		self.rjs.joint_state.position[2] = self.m3_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m4_command_callback(self):
		self.rjs.joint_state.position[3] = self.m4_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m5_command_callback(self):
		self.rjs.joint_state.position[4] = self.m5_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m6_command_callback(self):
		self.rjs.joint_state.position[5] = self.m6_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m7_command_callback(self):
		self.rjs.joint_state.position[6] = self.m7_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m8_command_callback(self):
		self.rjs.joint_state.position[7] = self.m8_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m9_command_callback(self):
		self.rjs.joint_state.position[8] = self.m9_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m10_command_callback(self):
		self.rjs.joint_state.position[9] = self.m10_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

class MenuLeftLegScreen(Screen):
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	
	rjs = RobotJointState()

	#l_leg_hip_y properties
	m1_pos_slider = ObjectProperty(None)

	#l_leg_hip_r properties
	m2_pos_slider = ObjectProperty(None)

	#l_leg_hip_p properties
	m3_pos_slider = ObjectProperty(None)

	#l_leg_kn_p properties
	m4_pos_slider = ObjectProperty(None)

	#l_leg_an_p properties
	m5_pos_slider = ObjectProperty(None)

	#l_leg_an_r properties
	m6_pos_slider = ObjectProperty(None)
	pass

	def __init__(self, **kwargs):
		super(MenuLeftLegScreen, self).__init__(**kwargs)
		self.command_sub = rospy.Subscriber("joint_states", JointState,
											self.update_rjs, queue_size=10)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()

	def update_rjs(self, msg):
		self.rjs.copy(msg)
		
	def m1_command_callback(self):
		self.rjs.joint_state.position[32] = self.m1_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m2_command_callback(self):
		self.rjs.joint_state.position[31] = self.m2_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m3_command_callback(self):
		self.rjs.joint_state.position[33] = self.m3_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m4_command_callback(self):
		self.rjs.joint_state.position[34] = self.m4_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m5_command_callback(self):
		self.rjs.joint_state.position[35] = self.m5_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m6_command_callback(self):
		self.rjs.joint_state.position[36] = self.m6_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

class MenuRightLegScreen(Screen):
	url = 'http://localhost:8080/snapshot?topic=/rviz1/camera1/image&type=png'
	image_path = StringProperty("robotImage.png")
	urllib.request.urlretrieve(url, "robotImage.png")
	img = ObjectProperty(source = "robotImage.png")
	
	rjs = RobotJointState()

	#r_leg_hip_y properties
	m1_pos_slider = ObjectProperty(None)

	#r_leg_hip_r properties
	m2_pos_slider = ObjectProperty(None)

	#r_leg_hip_p properties
	m3_pos_slider = ObjectProperty(None)

	#r_leg_kn_p properties
	m4_pos_slider = ObjectProperty(None)

	#r_leg_an_p properties
	m5_pos_slider = ObjectProperty(None)

	#r_leg_an_r properties
	m6_pos_slider = ObjectProperty(None)
	pass

	def __init__(self, **kwargs):
		super(MenuRightLegScreen, self).__init__(**kwargs)
		self.command_sub = rospy.Subscriber("joint_states", JointState,
											self.update_rjs, queue_size=10)
		
	def change_image(self, path):
		urllib.request.urlretrieve(self.url, path)
		os.system("mv new_robotImage.png robotImage.png")
		self.img.reload()
	
	def update_rjs(self, msg):
		self.rjs.copy(msg)
		
	def m1_command_callback(self):
		self.rjs.joint_state.position[26] = self.m1_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m2_command_callback(self):
		self.rjs.joint_state.position[25] = self.m2_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m3_command_callback(self):
		self.rjs.joint_state.position[27] = self.m3_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m4_command_callback(self):
		self.rjs.joint_state.position[28] = self.m4_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")

	def m5_command_callback(self):
		self.rjs.joint_state.position[29] = self.m5_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
	
	def m6_command_callback(self):
		self.rjs.joint_state.position[30] = self.m6_pos_slider.value * math.pi/180
		self.rjs.joint_state.header.stamp = rospy.Time.now()
		self.rjs.joint_state.header.seq += 1
		joint_pub.publish(self.rjs.joint_state)
		self.change_image("new_robotImage.png")
		
class IDScreen(Screen):
	pass
class TranscendGUIApp(MDApp):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		#rospy.init_node('kivy_app')
		#print("Created ros node!")
		#rospy.Subscriber("/bus0/ft_sensor0/ft_sensor_readings/wrench", WrenchStamped, wrench_callback)
		#print("Subscribed to this topic")
		#self.screen=Builder.load_file('ros_gui.kv') #load the .kv file for the main window
		self.screen=Builder.load_string(KV)
		# TO-DO- USE getcwd()
		
	def build(self):
		sm = ScreenManager()
		sm.add_widget(MenuScreen(name='home'))
		# sm.add_widget(MenuHeadScreen(name='home_head_control'))
		# sm.add_widget(MenuTorsoScreen(name='home_torso_control'))
		# sm.add_widget(MenuLeftArmScreen(name='home_leftarm_control'))
		# sm.add_widget(MenuRightArmScreen(name='home_rightarm_control'))
		# sm.add_widget(MenuLeftLegScreen(name='home_leftleg_control'))
		# sm.add_widget(MenuRightLegScreen(name='home_rightleg_control'))
		sm.add_widget(IDScreen(name='id'))
		sm.add_widget(LIDARScreen(name='lidar'))
		sm.add_widget(RealsenseScreen(name='realsense'))
		sm.add_widget(IMUScreen(name='imu'))
		sm.add_widget(FTScreen(name='ft'))

		# menu_items = [
		#	 {
		#		 "viewclass": "OneLineListItem",
		#		 "text": f"Item {i}",
		#		 "height": dp(56),
		#		 "on_release": lambda x=f"Item {i}": self.menu_callback(x),
		#	  } for i in range(5)
		# ]
		menu_items = [
			{
				"viewclass": "OneLineListItem",
				"text": "Head",
				"on_release": lambda *args: self.set_screen('home_head_control')
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Torso",
				"on_release": lambda *args: self.set_screen('home_torso_control')
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Left Arm",
				"on_release": lambda *args: self.set_screen('home_leftarm_control')
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Right Arm",
				"on_release": lambda *args: self.set_screen('home_rightarm_control')
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Left Leg",
				"on_release": lambda *args: self.set_screen('home_leftleg_control')
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Right Leg",
				"on_release": lambda *args: self.set_screen('home_rightleg_control')
			}
		]
		self.menu = MDDropdownMenu(
			items=menu_items,
			width_mult=4,
		)
		# screen = Builder.load_string(screen_helper)
		return sm
	
	
	def callback(self, button):
		self.menu.caller = button
		self.menu.open()

	# def menu_callback(self, text_item):
	#	 self.menu.dismiss()
	#	 Snackbar(text=text_item).open()
	
	def set_screen(self, screen_name):
		self.root.current = screen_name
	
	# def on_start(self):
	#	 # for i in range(3):
	#	 #		 self.root.ids.tabs.add_widget(Tab(title=f"LiDAR {i}"))
	#	 for name_tab in list(md_icons.keys())[15:18]:
	#		 self.root.ids.tabs.add_widget(Tab(icon=name_tab, title=name_tab))

	def on_tab_switch(
			self, instance_tabs, instance_tab, instance_tab_label, tab_text
	):
		"""
		Called when switching tabs
		:type instance_tabs: <kivymd.uix.tab.MDTabs object>;
		:param instance_tab: <__main__.Tab object>;
		:param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
		:param tab_text: text or name icon of tab;
		"""
		#print(f"{instance_tabs} {instance_tab_label} {tab_text}")
		count_icon = instance_tab.icon

		if count_icon == 'motion-sensor':
			#self.root.screen_manager.current = 'screen1'
			self.root.current = 'lidar'
		elif count_icon == 'camera-outline':
			self.root.current = 'realsense'
		elif count_icon == 'chart-waterfall':
			self.root.current = 'imu'
		elif count_icon == 'cog':
			self.root.current = 'ft'

#run ft sensor
def run_ros_launch_1():
	command1 = "roslaunch bota_demo BFT_LAXS_SER_M8_1.launch"
	subprocess.run(command1, shell=True)
	
def run_ros_launch_2():
	command2 = "roslaunch bota_demo BFT_LAXS_SER_M8_2.launch"
	subprocess.run(command2, shell=True)


# Create a thread for running the command
#command_thread1 = threading.Thread(target = run_ros_launch_1)
#command_thread2 = threading.Thread(target = run_ros_launch_2)

# Start the command thread
#command_thread1.start()
#command_thread2.start()
#time.sleep(10)

rospy.init_node('humanoid_gui', anonymous=True)
#pub = rospy.Publisher('set_position', SetPosition, queue_size=10)

print("***********Waiting***********")
# Run the Kivy app in the main thread
TranscendGUIApp().run()

print("Can I reach here??")

while(True):
	pass
