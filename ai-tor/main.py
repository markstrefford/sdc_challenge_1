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
  
def udacity_data_generator(batchsize, nepochs, path="/media/aitor/Data/udacity/dataset2-clean.bag", shift=None, randomize=False):
    if randomize:
        #Randomized data generator (shift optional). Memory expensive
        while 1:
            data = utils.load_randomized_udacity_dataset(path, shift)
            for i in range(0,nepochs):
                start = i*batchsize
                end = (i+1)*batchsize
                yield (data[0][start:end], data[1][start:end])
    else:
        #Not shited sequential data generator
        if (shift is None):
            while 1:
                bag = rosbag.Bag(path)
                x = np.empty([batchsize, 66, 200, 3])
                y = np.empty([batchsize, 1])
        
                i = 0;
                for topic,msg,t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
                    if(topic == '/vehicle/steering_report'):
                        current_steering = msg.steering_wheel_angle
                    elif(topic == '/center_camera/image_color'):
                        x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                        y[i] = np.array([current_steering]);
                        i = i + 1

                    if(i == batchsize):
                        i = 0
                        yield (x,y)
                bag.close()
        else:
            #Shifted sequential data generator
            while 1:
                bag = rosbag.Bag(path)
                x = np.empty([batchsize, 66, 200, 3])
                y = np.empty([batchsize, 1])
    
                i = 0
                current_steering = 0;
                for topic,msg,t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color',  '/left_camera/image_color', '/right_camera/image_color']):
                    if(topic == '/vehicle/steering_report'):
                        current_steering = msg.steering_wheel_angle
                    elif(topic == '/center_camera/image_color'):
                        x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                        y[i] = np.array([current_steering]);
                        i = i + 1
                    elif(topic == '/left_camera/image_color'):
                        x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                        y[i] = np.array([current_steering + shift]);
                        i = i + 1
                    elif(topic == '/right_camera/image_color'):
                        x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                        y[i] = np.array([current_steering - shift]);
                        i = i + 1
            
                    if(i == batchsize):
                        i = 0
                        yield (x, y)
            
                bag.close()
                

# Train model
val_data = utils.load_randomized_udacity_dataset("/media/aitor/Data/udacity/dataset-clean.bag")

model = nnmodel.getNNModel(reg_lambda=10)
#sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
optimizer = Adam()
model.compile(optimizer=optimizer, loss="mse")
stopping_callback = EarlyStopping(patience=20)

model.fit_generator(
    udacity_data_generator(100, 500),
    samples_per_epoch=100,
    nb_epoch=500,
    validation_data=val_data,
    callbacks=[stopping_callback]
)

response = utils.query_yes_no("Training session has finished. Do you want to save the model?")
if response:
    model.save("/media/aitor/Data/udacity/model.h5")

#out = model.predict(im)
