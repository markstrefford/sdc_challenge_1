#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 19:01:55 2016

@author: aitor
"""

from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout, BatchNormalization
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.regularizers import l2

#Based on NVIDIA's end-to-end paper: https://arxiv.org/pdf/1604.07316v1.pdf
#Depending on the training performance, normalization, pooling, dropout and zeropadding layers could be added
def getNNModel(weights_path=None):

    ch, width, height = 3, 200, 66
    reg_lambda = 0.1;
    
    model = Sequential()
    
    model.add(BatchNormalization(mode=0, axis=3, input_shape=(height, width, ch)))
	
    model.add(Convolution2D(24, 5, 5, subsample=(2,2), border_mode='same', activation='relu',W_regularizer=l2(reg_lambda), name='conv1'))
    #model.add(MaxPooling2D((2,2)))

    model.add(Convolution2D(36, 5, 5, subsample=(2,2), border_mode='same', activation='relu',W_regularizer=l2(reg_lambda), name='conv2'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    #model.add(MaxPooling2D((2,2)))

    model.add(Convolution2D(48, 5, 5, subsample=(2,2), border_mode='same', activation='relu',W_regularizer=l2(reg_lambda), name='conv3'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    #model.add(MaxPooling2D((2,2)))

    model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu',W_regularizer=l2(reg_lambda), name='conv4'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    #model.add(MaxPooling2D((2,2)))

    model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu',W_regularizer=l2(reg_lambda), name='conv5'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    #model.add(MaxPooling2D((2,2)))
    
    model.add(Flatten())
    
    model.add(Dense(100, activation='relu',W_regularizer=l2(reg_lambda), name='dense_1'))
    model.add(Dropout(0.5))
    model.add(Dense(50, activation='relu',W_regularizer=l2(reg_lambda), name='dense_2'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='relu',W_regularizer=l2(reg_lambda), name='dense_3'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='linear',W_regularizer=l2(reg_lambda), name='output'))
    
    if weights_path:
        model.load_weights(weights_path)
    
    return model