# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:38:10 2016

@author: aitor
"""
import rosbag
import utils

datafile = utils.get_datafile()
bag = rosbag.Bag(datafile)

topics = bag.get_type_and_topic_info()
#print topics[1]
print "/center_camera/image_color: {}".format(bag.get_message_count('/center_camera/image_color'))
print "/left_camera/image_color: {}".format(bag.get_message_count('/left_camera/image_color'))
print "/right_camera/image_color: {}".format(bag.get_message_count('/right_camera/image_color'))
print "/center_camera/image_color/compressed: {}".format(bag.get_message_count('/center_camera/image_color/compressed'))
print "/left_camera/image_color/compressed: {}".format(bag.get_message_count('/left_camera/image_color/compressed'))
print "/right_camera/image_color/compressed: {}".format(bag.get_message_count('/right_camera/image_color/compressed'))
print "/vehicle/throttle_report: {}".format(bag.get_message_count('/vehicle/throttle_report'))
print "/vehicle/steering_report: {}".format(bag.get_message_count('/vehicle/steering_report'))
print "/vehicle/brake_report: {}:".format(bag.get_message_count('/vehicle/brake_report'))
print "/vehicle/filtered_accel: {}:".format(bag.get_message_count('/vehicle/filtered_accel'))
print "/vehicle/wheel_speed_report: {}:".format(bag.get_message_count('/vehicle/wheel_speed_report'))
