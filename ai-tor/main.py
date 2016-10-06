#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:56:59 2016

@author: aitor
"""
import rosbag
import nnmodel
from keras.optimizers import SGD

datasetsDir = "/media/aitor/Data/"
bag = rosbag.Bag(datasetsDir + "dataset.bag")

# Train model
model = nnmodel.getNNmodel()
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(optimizer=sgd, loss='mse')


#out = model.predict(im)