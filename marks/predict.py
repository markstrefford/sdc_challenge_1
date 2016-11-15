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
import argparse
import pandas as pd


# Parse arguments
# --model / -m : Trained model to import
# --csv / -c : CSV file containing images, original steering, etc. (typically a validation set of viewing model predictions vs actuals)
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", help="trained model to import")
parser.add_argument("-c", "--csv", help="csv of images, steering angles, etc. to use")
args = parser.parse_args()

# Do we have a trained model argument
if args.model:
    model_path=args.model
else:
    model_path="../model/trained_model.h5"

# Load model
print "Loading trained model {}".format(model_path)
model = load_model(model_path)

# Now look for csv of validation data to load
if args.csv:
    validation_data = True
    csv_path = args.csv
    print "Preparing validation data at {}...".format(csv_path)
    test_df = pd.read_csv(csv_path)
else:
    test_df=pd.DataFrame()
    test_data_path = os.path.join(utils.test_data_path, 'center')  # '../data/Challenge 2/test/center'
    print "Preparing test data at {}...".format(test_data_path)
    test_df['filename'] = os.listdir(test_data_path)
    test_df['imagepath'] = test_data_path
    test_df['angle'] = False    # Means we don't have an actual
    test_df['speed'] = 10       # Assumed speed

# Setup image dimensions
ch, width, height = utils.ch, utils.width, utils.height

num_images = test_df.shape[0]
print "Found {} test images.".format(num_images)

# Step through images and display with steering path
x = np.zeros((1, 3, 200, 66), dtype=np.uint8)

for idx, test_row in test_df:
    img_path=test_row['filename']
    print "Image {}".format(img_path)
    image = cv2.imread(os.path.join(test_data_path,img_path))
    x[0, :, :, :] = cv2.resize(image, (width, height)).transpose(2,1,0)
    y = model.predict(x, batch_size=1)[0][0]

    angle = test_df['angle']
    if angle != False:
        utils.draw_path_on(image, test_row['speed'], test_row['angle']) # Actual (if it exists)
    speed = 10                                          # Assumption for now, we don't have the value in the test data!!
    utils.draw_path_on(image, speed, y, (0, 255, 0))    # Predicted

    cv2.imshow('Udacity challenge 2 - predicted angle viewer', image)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

    print "Steering angle: {} / Speed: {}".format(y, speed)  #, speed)
    #i += 1

cv2.destroyAllWindows()

