#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:39 2016

@author: marks
"""

import os
import nnmodel
import utils
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.utils.visualize_util import plot
import cv2
from keras.models import load_model
import numpy as np


# Train model--------------------
#model = nnmodel.getNNModel()
#optimizer = Adam(lr=1e-4)
#model.compile(optimizer, loss="mse")
#plot(model, to_file='model.png')
#stopping_callback = EarlyStopping(patience=5)

model = load_model("../model/trained_model.h5")

train_data_path = utils.train_data_path  #'../data/Challenge 2/train'
test_data_path = os.path.join(utils.test_data_path, 'center')   #'../data/Challenge 2/test/center'
ch, width, height = utils.ch, utils.width, utils.height

# TODO:
# Find subdirectories
# Create a train and validation list at the top-level subdirectory level
# Modify fit_generator to step through the list of images for train
# Modify validation code??

print "Preparing test data at {}...".format(test_data_path)
test_paths = utils.get_test_image_list(test_data_path)
#print train_paths
#img_df = utils.get_image_list(train_paths)
#images_df = images_df = img_df.loc[img_df['frame_id']=='center_camera'].reset_index(drop=True) #utils.get_image_list(train_paths)
num_images = len(test_paths)
print "Found {} test images.".format(num_images)


#train_image_idx, valid_image_idx = utils.split_train_and_validate(images_df, 0.90)  # Start with a 90/10 split of train/validation
#num_training_samples = len(train_image_idx)
#num_valid_samples = len(valid_image_idx)
#print train_image_idx[:10]
#print valid_image_idx[:10]

#train_paths = ["../data/center_camera/shuffled_list.txt", "../data/lft_camera/shuffled_list.txt", "../data/right_camera/shuffled_list.txt"]
#val_paths = ["/home/aitor/udacity/center_camera/list_shuffled_val.txt", "/home/aitor/udacity/left_camera/list_shuffled_val.txt", "/home/aitor/udacity/right_camera/list_shuffled_val.txt"]

#train_generator = utils.data_generator(128, images_df, train_image_idx, get_speed=False)
#val_data = utils.data_generator(128, images_df, valid_image_idx, get_speed=False)

# history = model.fit_generator(
#     train_generator,
#     samples_per_epoch=num_training_samples,
#     nb_epoch=5,
#     validation_data=val_data,
#     nb_val_samples=num_valid_samples
#     #callbacks=[stopping_callback]
# )

x = np.zeros((1, 3, 200, 66), dtype=np.uint8)

for img_path in test_paths:
    print "Image {}".format(img_path)
    image = cv2.imread(os.path.join(test_data_path,img_path))
    x[0, :, :, :] = cv2.resize(image, (width, height)).transpose(2,1,0)
    y = model.predict(x, batch_size=1)[0][0]

    speed = 10  # Assumption for now, we don't have the value in the test data!!
    utils.draw_path_on(image, speed, y, (0, 255, 0))

    cv2.imshow('Udacity challenge 2 - predicted angle viewer', image)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

    print "Steering angle: {} / Speed: {}".format(y, speed)  #, speed)
    #i += 1

cv2.destroyAllWindows()

#-----------------------------

#Save it if it is ok-----------
#response = utils.query_yes_no("Training session has finished. Do you want to save the model?")
#if response:
#model.save("../model/trained_model.h5")
#-----------------------------

#Show results-----------------
#utils.run_test_viewer(model)
#----------------------------
