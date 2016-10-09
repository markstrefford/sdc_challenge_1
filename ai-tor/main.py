#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:56:59 2016

@author: aitor
"""

import nnmodel
import rosbag
import cv2
import numpy as np
from cv_bridge import CvBridge
from keras.optimizers import Adam

datasetsDir = "/media/aitor/Data1/"
batch_size = 10000

def udacity_data_generator(path, batch_size):
    while 1:
        bag = rosbag.Bag(path)
        x = np.empty([batch_size, 66, 200, 3])
        y = np.empty([batch_size, 1])
        i = 0;
        for topic,msg,t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
            if(topic == '/vehicle/steering_report'):
                y[i] = np.array([msg.steering_wheel_angle])
            if(topic == '/center_camera/image_color'):
                x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                i = i + 1

            if(i == batch_size):
                i = 0
                yield (x,y)
        bag.close()

#udacity_data_generator(datasetsDir + "dataset.bag")

# Train model
model = nnmodel.getNNModel()

#sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
adam = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(optimizer=adam, loss="mse")


model.fit_generator(
    udacity_data_generator(datasetsDir + "dataset.bag", batch_size),
    samples_per_epoch=batch_size,
    nb_epoch=200,
    validation_data=udacity_data_generator(datasetsDir + "dataset.bag", 1000),
    nb_val_samples=1000,
)

#out = model.predict(im)