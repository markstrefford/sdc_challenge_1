#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:56:59 2016

@author: aitor
"""

import os
import nnmodel
import utils
import numpy as np
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.utils.visualize_util import plot
from datetime import datetime


# Train model--------------------
model = nnmodel.getNNModel()
optimizer = Adam(lr=1e-4)
model.compile(optimizer, loss="mse")
plot(model, to_file='model.png')
stopping_callback = EarlyStopping(patience=5)

train_data_path = utils.train_data_path  #'../data/Challenge 2/train'
test_data_path = utils.test_data_path   #'../data/Challenge 2/test'
ch, width, height = utils.ch, utils.width, utils.height

# TODO:
# Find subdirectories
# Create a train and validation list at the top-level subdirectory level
# Modify fit_generator to step through the list of images for train
# Modify validation code??

print "Preparing training and validation data..."
train_paths = utils.get_data_paths(train_data_path)
train_path_list, valid_path_list = utils.split_train_and_validate(train_paths, 0.8)    # Use 80% for training, 20% for validation

# Get list of training images
#train_img_df = utils.get_image_list(train_path_list)
#train_images_df = train_img_df.loc[train_img_df['frame_id']=='center_camera'].reset_index(drop=True) #utils.get_image_list(train_paths)
train_images_df = utils.get_image_df(train_path_list)
num_train_images = train_images_df.shape[0]
print "Found {} training images.".format(num_train_images)

# Get list of validation images (TODO: Be DRY here!!)
#valid_img_df = utils.get_image_list(valid_path_list)
#valid_images_df = valid_img_df.loc[valid_img_df['frame_id']=='center_camera'].reset_index(drop=True) #utils.get_image_list(train_paths)
valid_images_df = utils.get_image_df(valid_path_list)
num_valid_images = valid_images_df.shape[0]
print "Found {} validation images.".format(num_valid_images)
valid_images_df.to_csv('../data/Challenge 2/validate_list.csv')     # TODO: Move this to somewhere else and parameterise

# Now set up generators for training
train_generator = utils.data_generator(128, train_images_df, get_speed=False)
val_data = utils.data_generator(128, valid_images_df, get_speed=False)

history = model.fit_generator(
    train_generator,
    samples_per_epoch=num_train_images,
    nb_epoch=5,
    validation_data=val_data,
    nb_val_samples=num_valid_images
    #callbacks=[stopping_callback]
)


#-----------------------------

#Save it if it is ok-----------
#response = utils.query_yes_no("Training session has finished. Do you want to save the model?")
#if response:

model.save("../model/trained_model_{}.h5".format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S')))
#-----------------------------

#Show results-----------------
#utils.run_test_viewer(model)
#----------------------------
