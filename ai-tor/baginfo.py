# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:38:10 2016

@author: aitor
"""
import utils
import rosbag

#print bag.get_message_count('/left_camera/image_color')
#print bag.get_message_count('/right_camera/image_color')

#utils.crop_rosbag_file("/media/aitor/Data/udacity/dataset.bag", "/media/aitor/Data/udacity/dataset-croped.bag", 1700)
#utils.clean_dataset("/media/aitor/Data/udacity/dataset1.bag", "/media/aitor/Data/udacity/dataset1-clean.bag")
#utils.clean_dataset("/media/aitor/Data/udacity/dataset2.bag", "/media/aitor/Data/udacity/dataset2-clean.bag")
#utils.clean_dataset("/media/aitor/Data/udacity/dataset3.bag", "/media/aitor/Data/udacity/dataset3-clean.bag")

#utils.rosbag_to_jpeg("/media/aitor/Data/udacity/dataset1-clean.bag", "/media/aitor/Data/udacity/images1/")
#utils.rosbag_to_jpeg("/media/aitor/Data/udacity/dataset2-clean.bag", "/media/aitor/Data/udacity/images2/")
#utils.rosbag_to_jpeg("/media/aitor/Data/udacity/dataset3-clean.bag", "/media/aitor/Data/udacity/images3/")

utils.shuffle_list("/media/aitor/Data/udacity/images1/center_camera/list.txt", "/media/aitor/Data/udacity/images1/center_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images2/center_camera/list.txt", "/media/aitor/Data/udacity/images2/center_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images3/center_camera/list.txt", "/media/aitor/Data/udacity/images3/center_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images1/left_camera/list.txt", "/media/aitor/Data/udacity/images1/left_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images2/left_camera/list.txt", "/media/aitor/Data/udacity/images2/left_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images3/left_camera/list.txt", "/media/aitor/Data/udacity/images3/left_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images1/right_camera/list.txt", "/media/aitor/Data/udacity/images1/right_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images2/right_camera/list.txt", "/media/aitor/Data/udacity/images2/right_camera/list_shuffled.txt")
utils.shuffle_list("/media/aitor/Data/udacity/images3/right_camera/list.txt", "/media/aitor/Data/udacity/images3/right_camera/list_shuffled.txt")

