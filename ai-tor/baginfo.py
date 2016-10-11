# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:38:10 2016

@author: aitor
"""
import rosbag
import utils

bag = rosbag.Bag(datafile)
print bag.get_message_count('/center_camera/image_color')
print bag.get_message_count('/left_camera/image_color')
print bag.get_message_count('/right_camera/image_color')
