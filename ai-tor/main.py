#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:56:59 2016

@author: aitor
"""

import nnmodel
import utils
import rosbag
import cv2
import numpy as np
from cv_bridge import CvBridge
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping                

# Train model--------------------
model = nnmodel.getNNModel(reg_lambda=10)
optimizer = Adam()
model.compile(optimizer=optimizer, loss="mse")
stopping_callback = EarlyStopping(patience=5)

model.fit_generator(
    utils.udacity_data_generator(100, path="/media/aitor/Data/udacity/dataset3-clean.bag"),
    samples_per_epoch=100,
    nb_epoch=500,
    validation_data=utils.udacity_data_generator(100, path="/media/aitor/Data/udacity/dataset2-clean.bag"),
    callbacks=[stopping_callback]
)
#-----------------------------

#Save it if it is ok-----------
response = utils.query_yes_no("Training session has finished. Do you want to save the model?")
if response:
    model.save("/media/aitor/Data/udacity/model.h5")
#-----------------------------

#Show results-----------------
real_steering = 0
x = np.empty([1, 66, 200, 3])
for topic, msg, t in rosbag.Bag("/media/aitor/Data/udacity/dataset-clean.bag").read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
	if(topic == '/vehicle/steering_report'):
		real_steering = msg.steering_wheel_angle
	elif(topic == '/center_camera/image_color'):
		x[0] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
		y = model.predict(x, batch_size=1)
		print "real: " + str(real_steering) + ", predicted: " + str(y)
#----------------------------
