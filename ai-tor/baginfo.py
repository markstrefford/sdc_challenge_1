# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:38:10 2016

@author: aitor
"""
import utils

utils.prepare_dataset(["/media/aitor/Data/udacity/dataset1.bag", "/media/aitor/Data/udacity/dataset2.bag", "/media/aitor/Data/udacity/dataset3.bag", "/media/aitor/Data/udacity/dataset4.bag"], "/home/aitor/udacity/")

utils.shuffle_list("/home/aitor/udacity/center_camera/list.txt", "/home/aitor/udacity/center_camera/list_shuffled.txt")
utils.shuffle_list("/home/aitor/udacity/right_camera/list.txt", "/home/aitor/udacity/right_camera/list_shuffled.txt")
utils.shuffle_list("/home/aitor/udacity/left_camera/list.txt", "/home/aitor/udacity/left_camera/list_shuffled.txt")

