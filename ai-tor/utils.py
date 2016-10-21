import os
import rospy
import rosbag
import cv2
import numpy as np
from cv_bridge import CvBridge
import sys
import h5py
import glob
import matplotlib.pyplot as plt

def udacity_data_generator(batchsize, path="/media/aitor/Data/udacity/images3/", list_name="list_shuffled", include_shift=False):
	while 1:
		files = [open(path + "center_camera/" + list_name + ".txt")]
		
		if include_shift:
			files.append(open(path + "left_camera/" + list_name + ".txt"))
			files.append(open(path + "right_camera/" + list_name + ".txt"))
	
		i = 0
		files = map(iter, files)
		while files:
			for it in files:
				try:
					line = it.next()
					imagepath = os.path.dirname(it.name) + "/" + line.split()[0] + ".jpg"
                			x[i,:,:,:] = cv2.resize(cv2.imread(imagepath), (200, 66))
                			y[i] = float(line.split()[1])
					i = i + 1
					
					if(i == batchsize):
						i = 0
						yield(x,y)
						
				except StopIteration:
					files.remove(it)
		
		center_file.close()
		left_file.close()
		right_file.close()

def rosbag_to_jpeg(inpath, outpath):
	cvbridge = CvBridge()
	bag = rosbag.Bag(inpath)
	left_camera_path = outpath + "left_camera/"
	right_camera_path = outpath + "right_camera/"
	center_camera_path = outpath + "center_camera/"

	if not os.path.exists(outpath):
		os.makedirs(outpath)

	if not os.path.exists(left_camera_path):
		os.makedirs(left_camera_path)

	if not os.path.exists(right_camera_path):
		os.makedirs(right_camera_path)

	if not os.path.exists(center_camera_path):
		os.makedirs(center_camera_path)

	center_file = open(center_camera_path + "list.txt", 'w')
	right_file = open(right_camera_path + "list.txt", 'w')
	left_file = open(left_camera_path + "list.txt", 'w')

	current_steering = -1
	center_i = 0
	left_i = 0
	right_i = 0
	for topic, msg, t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color', '/left_camera/image_color', '/right_camera/image_color', '/center_camera/image_color/compressed', '/left_camera/image_color/compressed', '/right_camera/image_color/compressed']):
		if (topic == '/vehicle/steering_report'):
			current_steering = msg.steering_wheel_angle

		if (current_steering != -1):
			if (topic == '/center_camera/image_color'):
				img = cv2.resize(cvbridge.imgmsg_to_cv2(msg, "bgr8"), (200, 66))
				cv2.imwrite(center_camera_path + str(center_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
				center_file.write(str(center_i) + " " + str(current_steering) + "\n")
				center_i = center_i + 1
			elif (topic == '/left_camera/image_color'):
				img = cv2.resize(cvbridge.imgmsg_to_cv2(msg, "bgr8"), (200, 66))
				cv2.imwrite(left_camera_path + str(left_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
				left_file.write(str(left_i) + " " + str(current_steering) + "\n")
				left_i = left_i + 1
			elif (topic == '/right_camera/image_color'):
				img = cv2.resize(cvbridge.imgmsg_to_cv2(msg, "bgr8"), (200, 66))
				cv2.imwrite(right_camera_path + str(right_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
				right_file.write(str(right_i) + " " + str(current_steering) + "\n")
				right_i = right_i + 1
                        elif (topic == '/center_camera/image_color/compressed'):
                                img = cv2.resize(cvbridge.compressed_imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                                cv2.imwrite(center_camera_path + str(center_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                                center_file.write(str(center_i) + " " + str(current_steering) + "\n")
                                center_i = center_i + 1
                        elif (topic == '/left_camera/image_color/compressed'):
                                img = cv2.resize(cvbridge.compressed_imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                                cv2.imwrite(left_camera_path + str(left_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                                left_file.write(str(left_i) + " " + str(current_steering) + "\n")
                                left_i = left_i + 1
                        elif (topic == '/right_camera/image_color/compressed'):
                                img = cv2.resize(cvbridge.compressed_imgmsg_to_cv2(msg, "bgr8"), (200, 66))
                                cv2.imwrite(right_camera_path + str(right_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                                right_file.write(str(right_i) + " " + str(current_steering) + "\n")
                                right_i = right_i + 1

	bag.close()
	center_file.close()
	right_file.close()
	left_file.close()
			
                    

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
        

################################################################################
# Cleaning the Data
################################################################################

def clean_dataset(inpath, outpath):
    # Clean the rosbag
    print "start"
    with rosbag.Bag(outpath, 'w') as outbag:
        bag = rosbag.Bag(inpath)
        
        current_speed = 0
        j = 0
        r = np.random.uniform(0,1)
        print "opened file"
        for topic, msg, t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color',  '/left_camera/image_color', '/right_camera/image_color', '/center_camera/image_color/compressed',  '/left_camera/image_color/compressed', '/right_camera/image_color/compressed']):

            if (topic == '/vehicle/steering_report'):
                current_speed = msg.speed
                current_steering_msg = msg
                current_steering = msg.steering_wheel_angle
		current_time = t
		current_topic = topic
                
            elif (current_speed > 8.0): #an image
                if ((abs(current_steering) >= 0.1) or (r < 0.08)):
                    outbag.write(topic, msg, t)
                    j = j + 1
                    
                    if (j == 3): #one steering angle for every 3 images (left, right and center camera)
                        outbag.write(current_topic, current_steering_msg, current_time)
                        r = np.random.uniform(0,1)
			current_speed = 0
                        j = 0
