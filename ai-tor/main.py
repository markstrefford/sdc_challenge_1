#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:56:59 2016

@author: aitor
"""

import nnmodel
import utils
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping          
from keras.utils.visualize_util import plot


# Train model--------------------
model = nnmodel.getNNModel()
optimizer = Adam(lr=1e-4)
model.compile(optimizer, loss="mse")
plot(model, to_file='model.png')
stopping_callback = EarlyStopping(patience=5)

train_paths = ["/home/aitor/udacity/center_camera/list_shuffled.txt", "/home/aitor/udacity/left_camera/list_shuffled.txt", "/home/aitor/udacity/right_camera/list_shuffled.txt"]
#TODO generate validation lists
train_generator = utils.udacity_data_generator(241, train_paths)
val_data = utils.udacity_data_generator(1024, val_paths)

model.fit_generator(
    train_generator,
    samples_per_epoch=36391,
    nb_epoch=50,
    validation_data=val_data,
    nb_val_samples=1024
    #callbacks=[stopping_callback]
)
#-----------------------------

#Save it if it is ok-----------
response = utils.query_yes_no("Training session has finished. Do you want to save the model?")
if response:
	model.save("/media/aitor/Data/udacity/model.h5")
#-----------------------------

#Show results-----------------
   
#TODO: Integrate @marks code
#----------------------------
