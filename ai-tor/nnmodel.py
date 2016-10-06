#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 19:01:55 2016

@author: aitor
"""

from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D

#Based on NVIDIA's end-to-end paper: https://arxiv.org/pdf/1604.07316v1.pdf
#Depending on the training performance, normalization, pooling, dropout and zeropadding layers could be added
def getNNModel(weights_path=None):

    model = Sequential()
    
    model.add(Convolution2D(24, 5, 5, subsample=(2,2), activation='relu', name='conv1', input_shape=(3,66,200)))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    
    model.add(Convolution2D(36, 5, 5, subsample=(2,2), activation='relu', name='conv2'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    
    model.add(Convolution2D(48, 5, 5, subsample=(2,2), activation='relu', name='conv3'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    
    model.add(Convolution2D(64, 3, 3, activation='relu', name='conv4'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    
    model.add(Convolution2D(64, 3, 3, activation='relu', name='conv5'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    
    model.add(Flatten())
    
    model.add(Dense(100, activation='relu', name='dense_1'))
    #model.add(Dropout(0.5))
    model.add(Dense(50, activation='relu', name='dense_2'))
    #model.add(Dropout(0.5))
    model.add(Dense(10, activation='relu', name='dense_3'))
     #model.add(Dropout(0.5))
    model.add(Dense(1, activation='linear', name='output'))
    
    if weights_path:
        model.load_weights(weights_path)
    
    return model