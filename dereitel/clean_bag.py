import os.path
import rosbag
import matplotlib.pyplot as plt
import numpy as np

################################################################################
#
# Made by Fabi Eitel
#
# Prerequisites:
# Tool for merging https://bitbucket.org/daniel_dube/bagedit/wiki/Home
# 1. Merge both center cameras in dataset 3
# 2. Merge steering_report with camera_center data in all datasets (steering values are in: udacity-dataset_io_vehicle)
# 3. Uncomment from last part what needed
#
################################################################################


################################################################################
# Data locations
################################################################################
_inpath_3 = '/home/fabi/sdc/data/2016-10-10/udacity-dataset_sensor_camera_center_2016-10-11-13-23-02_0.bag_merged.bag_merged.bag'
_inpath_2 = '/home/fabi/sdc/data/udacity-dataset-2-2/udacity-dataset_sensor_camera_center_2016-10-09-03-47-05_0.bag_merged.bag'
_inpath_1 = '/home/fabi/sdc/data/udacity-dataset-2-1/udacity-dataset_sensor_camera_center_2016-10-09-05-49-13_0.bag_merged.bag'
_outpath_3 = '/home/fabi/sdc/data/2016-10-10/clean_dataset_3.bag'
_outpath_2 = '/home/fabi/sdc/data/udacity-dataset-2-2/clean_dataset_2.bag'
_outpath_1 = '/home/fabi/sdc/data/udacity-dataset-2-1/clean_dataset_1.bag'

################################################################################
# Exploratory Data Analyis
################################################################################
def eda_steering_angles(inpath):
    # Eploratory data analysis on the distribution of steering data
    steering_angles = []
    for topic, msg, t in rosbag.Bag(inpath).read_messages(topics=['/vehicle/steering_report']):
        current_speed = msg.speed
        if (current_speed > 8.0):
            steering_angles.append(msg.steering_wheel_angle)

    plt.hist(steering_angles)
    plt.title('Steering angles - Udacity Dataset')
    plt.show()

################################################################################
# Cleaning the Data
################################################################################

def clean_dataset(inpath, outpath):
    # Clean the rosbag
    print "start"
    with rosbag.Bag(outpath, 'w') as outbag:
         current_speed = 0
         current_steering = 0
         print "opened file"
         for topic, msg, t in rosbag.Bag(inpath).read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color', '/center_camera/image_color/compressed']):

             if (topic == '/vehicle/steering_report'):
                 current_speed = msg.speed
                 current_steering = msg.steering_wheel_angle

             if (current_speed > 8.0):
                 if (abs(current_steering) >= 0.1):
                     outbag.write(topic, msg, t)
                 elif (np.random.uniform(0, 1) < 0.08):
                     outbag.write(topic, msg, t)

################################################################################
# Running the functions
################################################################################

# Uncomment as desired
#clean_dataset(_inpath_3, _outpath_3)
#clean_dataset(_inpath_2, _outpath_2)
#clean_dataset(_inpath_1, _outpath_1)

#eda_steering_angles(_outpath_3)
#eda_steering_angles(_inpath_1)
#eda_steering_angles(_outpath_1)
