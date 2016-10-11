import os.path
import rosbag
import cv2
import numpy as np
from cv_bridge import CvBridge

def get_datafile():
    datafile = "dataset.bag"
    if os.path.exists("./data/" + datafile):
        datasetsDir = "./data/"
    elif os.path.exists("../data/" + datafile):
        datasetsDir = "../data/"
    else:
        datasetsDir = "/media/aitor/Data1/"
    return datasetsDir + datafile
    
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
    
def rosbag_to_numpy_file(path, outpath=None, shift=None):
    data = load_randomized_udacity_dataset(path, shift=shift)
    if (outpath is None):
        outpath = path + ".npz"
    np.savez(outpath, data[0], data[1])
    