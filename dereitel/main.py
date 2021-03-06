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
import tensorflow as tf
tf.python.control_flow_ops = tf

from keras import optimizers
from keras.callbacks import EarlyStopping
from keras.utils.visualize_util import plot


# Train model--------------------
model = nnmodel.getNNModel()
optimizer = 'Adam'
lr = 0.0005
methodToCall = getattr(optimizers, optimizer)
model.compile(optimizer=methodToCall(lr=lr), loss="mse")
plot(model, to_file='model.png')
stopping_callback = EarlyStopping(patience=10)

train_generator = utils.udacity_data_generator(512)
val_data = utils.validation_udacity_data(512)

hist = model.fit_generator(
    train_generator,
    samples_per_epoch= 2 * 50688, # depending on amount of images in dataset
    nb_epoch=1000,
    validation_data=val_data,
    nb_val_samples= 2 * 50688
    #callbacks=[stopping_callback]
)
print hist.history

#-----------------------------

#Save it if it is ok-----------
response = utils.query_yes_no("Training session has finished. Do you want to save the model?")
if response:
	model.save("/home/fabi/sdc/sdc_challenge_1/dereitel/model.h5")
#-----------------------------

#Show results-----------------
real_steering = 0
x = np.zeros((1, 66, 200, 3))
for topic, msg, t in rosbag.Bag("/home/fabi/sdc/data/udacity-dataset-2-1/clean_dataset_1.bag").read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
	if(topic == '/vehicle/steering_report'):
         real_steering = msg.steering_wheel_angle
	elif(topic == '/center_camera/image_color' or topic == '/center_camera/image_color/compressed'):
	 x[0,:,:,:] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
         y = model.predict(x, batch_size=1)
         print "real: " + str(real_steering) + ", predicted: " + str(y)

#----------------------------
