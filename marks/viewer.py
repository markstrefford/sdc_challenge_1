#!/usr/bin/env python
import argparse
#import sys
import numpy as np
#import h5py
import pygame
#import json
#from keras.models import model_from_json
import utils
import rosbag
import cv2
from cv_bridge import CvBridge


print "pygame.init()"
pygame.init()
scale = 4
frame_size = (200, 66)
#display_size = (frame_size[0] * scale, frame_size[1] * scale)
print "pygame.display.set_caption()"
pygame.display.set_caption("SDC Challenge 2 Data Viewer")
print "pygame.display.set_mode()"
screen = pygame.display.set_mode(frame_size, pygame.DOUBLEBUF)
print "pygame.surface.Surface()"
camera_surface = pygame.surface.Surface(frame_size, 0, 24).convert()

# Get frames and steering angle
print "utils.get_datafile()"
path = utils.get_datafile()
#print "utils.load_udacity_dataset()"
#data = utils.load_udacity_dataset(path)
#print "Image count: {}, steering angle count: {}".format(images.shape[0], steering_angles.shape[0])

# Main Loop

# Start by getting the images from the databag and displaying them one at a time
bag = rosbag.Bag(path)
nmessages =  bag.get_message_count('/center_camera/image_color')
x = np.empty([nmessages, frame_size[0], frame_size[1], 3])
y = np.empty([nmessages, 1])
i=0

# for topic, msg, t in bag.read_messages(
#         topics=['/vehicle/steering_report', '/center_camera/image_color', '/left_camera/image_color',
#                 '/right_camera/image_color']):
for topic, msg, t in bag.read_messages(
        topics=['/vehicle/steering_report', '/center_camera/image_color']):
    if (topic == '/vehicle/steering_report'):
        current_steering = msg.steering_wheel_angle
    elif (topic == '/center_camera/image_color'):
        img = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), frame_size).swapaxes(0,1)
        x[i] = img
        y[i] = np.array([current_steering]);

        # Display image
        #img_swapaxes = img.swapaxes(0,1)  #.swapaxes(0,1)
        #print img.shape, img.swap_axes.shape
        pygame.surfarray.blit_array(camera_surface, img)
        #scaled_surface = pygame.transform.scale(camera_surface, display_size, (0,0))
        #camera_surface_2x = pygame.transform.scale(img, display_size, (0,0))
        screen.blit(camera_surface, (0, 0))
        pygame.display.flip()

        i = i + 1


    # elif (topic == '/left_camera/image_color'):
    #     x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
    #     y[i] = np.array([current_steering + shift]);
    #     i = i + 1
    # elif (topic == '/right_camera/image_color'):
    #     x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
    #     y[i] = np.array([current_steering - shift]);
    #     i = i + 1


    if i % 100 == 0:
        print "Loaded image {}/{}".format(i, nmessages)

    if (i == nmessages):
        break


