import os.path
import rosbag
import cv2
import numpy as np
from cv_bridge import CvBridge
import sys

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

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
                             
def crop_rosbag_file(inpath, outpath, nummsgs):
    with rosbag.Bag(outpath, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(inpath).read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
            if nummsgs < 1:
                break
            nummsgs -= 1
            outbag.write(topic, msg, t)

def clean_rosbag_file(inpath, outpath):
	with rosbag.Bag(outpath, 'w') as outbag:
		current_speed = 0
		for topic, msg, t in rosbag.Bag(inpath).read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
			if (topic == '/vehicle/steering_report'):
				current_speed = msg.speed

			if (current_speed > 8.0):
				outbag.write(topic, msg, t)

