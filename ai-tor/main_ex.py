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

def load_randomized_udacity_dataset(path, shift=None):
    bag = rosbag.Bag(path)
    
    if (shift is not None):
        nmessages = bag.get_message_count('/center_camera/image_color')*3
        x = np.empty([nmessages, 66, 200, 3])
        y = np.empty([nmessages, 1])
    
        i = 0
        current_steering = 0
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
            
            if(i == nmessages):
                break
            
    else:
        nmessages = bag.get_message_count('/center_camera/image_color')
        x = np.empty([nmessages, 66, 200, 3])
        y = np.empty([nmessages, 1])
    
        i = 0
        current_steering = 0
        for topic,msg,t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
            if(topic == '/vehicle/steering_report'):
                current_steering = msg.steering_wheel_angle
            elif(topic == '/center_camera/image_color'):
                x[i] = cv2.resize(CvBridge().imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                y[i] = np.array([current_steering]);
                i = i + 1
            
            if(i == nmessages):
                break
            
    
    bag.close()

    #Shuffle
    rng_state = np.random.get_state()
    np.random.shuffle(x)
    np.random.set_state(rng_state)
    np.random.shuffle(y)

    return (x,y)    
            
def udacity_data_generator(path, batchsize, nepochs, shift=None, randomize=True):
    if randomize:
        #Randomized data generator (shift optional). Memory expensive
        while 1:
            data = load_randomized_udacity_dataset(path, shift)
            x = data[0]
            y = data[1]
            for i in range(0,nepochs):
                start = i*batchsize
                end = (i+1)*batchsize - 1
                yield (x[start:end], y[start:end])
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
model = nnmodel.getNNModel()
#sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
adam = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(optimizer=adam, loss="mse")
#model.train_on_batch(data[0], data[1])
model.fit_generator(
    udacity_data_generator("/media/aitor/Data1/dataset.bag", 100, 150, shift=1.0,randomize=False),
    samples_per_epoch=100,
    nb_epoch=150
    #validation_data=udacity_data_generator(datasetsDir + "dataset.bag", 1000),
    #nb_val_samples=1000,
)

#out = model.predict(im)