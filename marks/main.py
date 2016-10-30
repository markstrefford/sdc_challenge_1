#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:56:59 2016

@author: aitor
"""

import os
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

train_data_path = '/data/Challenge 2/train'
test_data_path = '/data/Challenge 2/test'

# TODO:
# Find subdirectories
# Create a train and validation list at the top-level subdirectory level
# Modify fit_generator to step through the list of images for train
# Modify validation code??

print "Preparing training and validation data..."
train_paths = utils.get_data_paths(train_data_path)
#print train_paths
images_df = utils.get_image_list(train_paths)
num_images = images_df.shape[0]
print "Found {} training images.".format(num_images)

train_image_idx, valid_image_idx = utils.split_train_and_validate(images_df, 0.90)  # Start with a 90/10 split of train/validation

#train_paths = ["../data/center_camera/shuffled_list.txt", "../data/lft_camera/shuffled_list.txt", "../data/right_camera/shuffled_list.txt"]
#val_paths = ["/home/aitor/udacity/center_camera/list_shuffled_val.txt", "/home/aitor/udacity/left_camera/list_shuffled_val.txt", "/home/aitor/udacity/right_camera/list_shuffled_val.txt"]

train_generator = utils.udacity_data_generator(128, images_df, train_image_idx)
val_data = utils.udacity_data_generator(1024, images_df, valid_image_idx)

history = model.fit_generator(
    train_generator,
    samples_per_epoch=200,  #20000
    nb_epoch=1,             #50,
    validation_data=val_data,
    nb_val_samples=10       #1024
    #callbacks=[stopping_callback]
)


#-----------------------------

#Save it if it is ok-----------
#response = utils.query_yes_no("Training session has finished. Do you want to save the model?")
#if response:
model.save("/data/models/model.h5")
#-----------------------------

#Show results-----------------
#utils.run_test_viewer(model)
#----------------------------
