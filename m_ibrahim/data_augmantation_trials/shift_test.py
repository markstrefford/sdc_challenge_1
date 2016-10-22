# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:38:10 2016

@author: mohamed-ibrahim
"""
import sys
sys.path.append("../../marks")
import utils

#utils.clean_dataset("/media/mohamed/New Volume/Udacity Dataset/dataset.bag", "/media/mohamed/New Volume/Udacity Dataset/dataset-clean.bag")


utils.rosbag_to_jpeg(["/media/mohamed/New Volume/Udacity Dataset/dataset.bag"], "/home/mohamed/udacity/")

#utils.shuffle_list("/home/aitor/udacity/center_camera/list.txt", "/home/aitor/udacity/center_camera/list_shuffled.txt")
