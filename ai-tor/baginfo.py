# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:38:10 2016

@author: aitor
"""
import rosbag

datasetsDir = "/media/aitor/Data1/"

bag = rosbag.Bag(datasetsDir + "dataset.bag")
print bag.get_message_count('/center_camera/image_color')