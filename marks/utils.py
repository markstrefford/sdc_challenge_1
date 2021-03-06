import os
import random
#import rosbag
#from cv_bridge import CvBridge
import cv2
import numpy as np
import sys
import scipy
from skimage import transform as tf
import pandas as pd

# Set default values, etc.
ch, width, height = 3, 200, 66

train_data_path = '../data/Challenge 2/train'
test_data_path = '../data/Challenge 2/test'

################################################################################
# Get a list of directories for training or testing purposes
# Assumes that the structure is /data/subdir1, /data/subdir2, etc...  (@marks)
################################################################################
def get_data_paths(data_path):
    paths = []
    subdirs = os.listdir(data_path)
    for dir in subdirs:
        if dir != '.DS_Store':    #Skip if the Mac OSX .DS_Store file getting in the way!
            path = os.path.join(data_path, dir)
            paths.append(path)
    return paths

################################################################################
# Get a list of images from the provided csv file(s)    (@marks)
################################################################################
def get_image_df(image_path_list):
    img_df = get_image_list(image_path_list)
    images_df = img_df.loc[img_df['frame_id']=='center_camera'].reset_index(drop=True)
    return images_df

################################################################################
# Get a list of images from the provided csv file(s)    (@marks)
################################################################################
def get_image_list(data_paths):
    images_df = pd.DataFrame()
    csv_filename = 'interpolated.csv'
    for path in data_paths:
        filename = os.path.join(path, csv_filename)
        image_df = pd.read_csv(filename)
        image_df['imagepath'] = path                        # Add in parent directory path so we can find the image later!!
        df = images_df.append(image_df, ignore_index=True)  # Not sure why I need to create a new DF first???
        images_df = df
    return images_df

################################################################################
# Get a list of testing images
################################################################################
# def get_test_image_list(data_path):
#     image_list = os.listdir(data_path)
#     return image_list

################################################################################
# Create an index of training and validation images  (@marks)
################################################################################
def split_train_and_validate(image_list, split = 1.0):
    main_index = range(len(image_list))
    # Take a random sample of drivers into the training list
    image_train_list = np.random.choice(image_list, int(len(main_index)*split), replace = False)
    # Take the remaining drivers into the validation list
    image_valid_list = [image for image in image_list if image not in image_train_list]
    return image_train_list, image_valid_list

################################################################################
# Generator for Keras over jpeg dataset (@ai-tor/@marks)
################################################################################
def data_generator(batchsize, image_list, get_speed = True, img_transpose = True, resize = True,
                   min_speed = 4, min_angle = 0.1, straight_road_prob = 0.2):


    if resize == False:
        width, height = 640, 480
    # Else go with the values set in utils
    else:
        width, height = 200, 66

    # while 1:
    if img_transpose == True:
        x = np.zeros((batchsize, ch, width, height), dtype=np.uint8)
    else:
        x = np.zeros((batchsize, height, width, ch), dtype=np.uint8)
    y = np.zeros(batchsize)
    z = np.zeros(batchsize)
    # iterators = []

    # for path in paths:
    #    iterators.append(open(path))

    i = 0
    # files = map(iter, iterators)
    # while files:
    while True:
        for idx in range(len(image_list)):
            # try:
            # line = it.next()
            # imagepath = os.path.dirname(it.name) + "/" + line.split()[0] + ".jpg"
            # Get data for training here... it's in the dataframe
            # print "{}{} / idx {}".format(flag, i, idx)
            # print "imagepath {}".format(image_list.at[idx, 'imagepath'])
            # print "filename {}".format(image_list.at[idx, 'filename'])
            # print image_list.loc[idx]
            steering = image_list.at[idx, 'angle']
            speed = image_list.at[idx, 'speed']
            imagepath = os.path.join(image_list.at[idx, 'imagepath'], image_list.at[idx, 'filename'])
            image = cv2.imread(imagepath)
            #cv2.imshow("Viewer", image)
            #try:
            img = cv2.resize(image, (width, height))

            # print "Processing image {} at index {}... {}, {}".format(i, idx, img.shape, steering)
            r = np.random.uniform(0, 1)
            if ((abs(steering) > min_angle) and speed >= min_speed) or (r < straight_road_prob):
                if img_transpose == True:
                    x[i, :, :, :] = img.transpose(2,1,0)   # Transpose the image to fit into the CNN later...
                else:
                    x[i, :, :, :] = img

                #x[i, :, :, :] = img.transpose(2,1,0)   # Transpose the image to fit into the CNN later...
                y[i] = float(steering)
                z[i] = float(speed)
                i = i + 1

                #except:
                # If resizing fails, skip...
                #print "udacity_data_generator():WARN - Image {}, shape {} failed to resize".format(imagepath, image.shape)
                #print "udacity_data_generator():WARN - Unexpected error resizing image: {}".format(sys.exc_info())

            if (i == batchsize):
                i = 0
                # print "x: {} / y: {}".format(x, y)
                if get_speed == True:
                    yield (x, y, z)
                else:
                    yield (x, y)

                    # except StopIteration:
                    #    it.close()
                    #    files.remove(it)

################################################################################
# Shuflles the lines of the lists generated by rosbag_to_jpeg (@ai-tor)
################################################################################
def shuffle_list(listpath, outpath):
    listfile = open(listpath)
    lines = []

    for line in listfile:
        lines.append(line)

    listfile.close()
    random.shuffle(lines)

    outfile = open(outpath, "w")
    for line in lines:
        outfile.write(line)
    outfile.close()


################################################################################
# Saves the rosbag files into jpeg (@ai-tor)
################################################################################
# def rosbag_to_jpeg(bagslist, outpath):
#     cvbridge = CvBridge()
#
#     left_camera_path = outpath + "left_camera/"
#     right_camera_path = outpath + "right_camera/"
#     center_camera_path = outpath + "center_camera/"
#
#     if not os.path.exists(outpath):
#         os.makedirs(outpath)
#
#     if not os.path.exists(left_camera_path):
#         os.makedirs(left_camera_path)
#
#     if not os.path.exists(right_camera_path):
#         os.makedirs(right_camera_path)
#
#     if not os.path.exists(center_camera_path):
#         os.makedirs(center_camera_path)
#
#     center_file = open(center_camera_path + "list.txt", 'w')
#     right_file = open(right_camera_path + "list.txt", 'w')
#     left_file = open(left_camera_path + "list.txt", 'w')
#
#     center_i = 0
#     left_i = 0
#     right_i = 0
#     for bagpath in bagslist:
#         bag = rosbag.Bag(bagpath)
#
#         current_steering = -1
#         current_speed = 0
#         for topic, msg, t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color', '/left_camera/image_color', '/right_camera/image_color', '/center_camera/image_color/compressed', '/left_camera/image_color/compressed', '/right_camera/image_color/compressed']):
#                 if (topic == '/vehicle/steering_report'):
#                     current_steering = msg.steering_wheel_angle
#                     current_speed = msg.speed
#
#                 if (current_steering != -1):
#                      if (topic == '/center_camera/image_color'):
#                         img = cv2.resize(cvbridge.imgmsg_to_cv2(msg, "bgr8"), (200, 66))
#                         cv2.imwrite(center_camera_path + str(center_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
#                         center_file.write(str(center_i) + " " + str(current_steering) + " " + str(current_speed) + "\n")
#                         center_i = center_i + 1
#                      elif (topic == '/left_camera/image_color'):
#                         img = cv2.resize(cvbridge.imgmsg_to_cv2(msg, "bgr8"), (200, 66))
#                         cv2.imwrite(left_camera_path + str(left_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
#                         left_file.write(str(left_i) + " " + str(current_steering + calculate_angle_from_shift(0.5, current_speed)[0]) + " " + str(current_speed) + "\n")
#                         left_i = left_i + 1
#                      elif (topic == '/right_camera/image_color'):
#                         img = cv2.resize(cvbridge.imgmsg_to_cv2(msg, "bgr8"), (200, 66))
#                         cv2.imwrite(right_camera_path + str(right_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
#                         right_file.write(str(right_i) + " " + str(current_steering + calculate_angle_from_shift(-0.5, current_speed)[0]) + " " + str(current_speed) + "\n")
#                         right_i = right_i + 1
#                      elif (topic == '/center_camera/image_color/compressed'):
#                         img = cv2.resize(cvbridge.compressed_imgmsg_to_cv2(msg, "bgr8"), (200, 66))
#                         cv2.imwrite(center_camera_path + str(center_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
#                         center_file.write(str(center_i) + " " + str(current_steering) + " " + str(current_speed) + "\n")
#                         center_i = center_i + 1
#                      elif (topic == '/left_camera/image_color/compressed'):
#                         img = cv2.resize(cvbridge.compressed_imgmsg_to_cv2(msg, "bgr8"), (200, 66))
#                         cv2.imwrite(left_camera_path + str(left_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
#                         left_file.write(str(left_i) + " " + str(current_steering + calculate_angle_from_shift(0.5, current_speed)[0]) + " " + str(current_speed) + "\n")
#                         left_i = left_i + 1
#                      elif (topic == '/right_camera/image_color/compressed'):
#                         img = cv2.resize(cvbridge.compressed_imgmsg_to_cv2(msg, "bgr8"), (200, 66))
#                         cv2.imwrite(right_camera_path + str(right_i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
#                         right_file.write(str(right_i) + " " + str(current_steering + calculate_angle_from_shift(-0.5, current_speed)[0]) + " " + str(current_speed) + "\n")
#                         right_i = right_i + 1
#
#         bag.close()
#
#     center_file.close()
#     right_file.close()
#     left_file.close()


################################################################################
# Cleaning the Data (removes stopped frames and most of straight lines @ai-tor, @deretiel)
################################################################################
# def clean_dataset(inpath, outpath):
#     # Clean the rosbag
#     print "start"
#     with rosbag.Bag(outpath, 'w') as outbag:
#         bag = rosbag.Bag(inpath)
#
#         current_speed = 0
#         j = 0
#         r = np.random.uniform(0,1)
#         print "opened file"
#         for topic, msg, t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color',  '/left_camera/image_color', '/right_camera/image_color', '/center_camera/image_color/compressed',  '/left_camera/image_color/compressed', '/right_camera/image_color/compressed']):
#
#             if (topic == '/vehicle/steering_report'):
#                 current_speed = msg.speed
#                 current_steering_msg = msg
#                 current_steering = msg.steering_wheel_angle
#                 current_time = t
#                 current_topic = topic
#
#             elif (current_speed > 8.0): #an image
#                 if ((abs(current_steering) >= 0.1) or (r < 0.2)):
#                     outbag.write(topic, msg, t)
#                     j = j + 1
#
#                     if (j == 3): #one steering angle for every 3 images (left, right and center camera)
#                         outbag.write(current_topic, current_steering_msg, current_time)
#                         r = np.random.uniform(0,1)
#                         current_speed = 0
#                         j = 0

################################################################################
# Calculates angle for shifted cameras (@mohamed_ibrahim)
################################################################################
def calculate_angle_from_shift(shift, speed, steer_ratio = 14.8, wheel_base = 2.85, dt = 1.5):
    #shift (m), v (m/s), dt (s)
    def F(x):
        phi_o = np.pi/2.0
        return (speed*dt/wheel_base)*np.sin(x) + x + phi_o - np.arccos(shift / (speed*dt))

    if speed >= 1:
        wheel_angle = scipy.optimize.broyden1(F, [0.1], f_tol=1e-5)
        return steer_ratio*wheel_angle  #rad
    else:
        return [0]

################################################################################
# Visualizes the results (based on comma.ai @marks)
################################################################################
# def run_test_viewer(model, bagpath = "/media/aitor/Data/udacity/dataset1.bag"):
rsrc = \
    [[43.45456230828867, 118.00743250075844],
     [104.5055617352614, 69.46865203761757],
     [114.86050156739812, 60.83953551083698],
     [129.74572757609468, 50.48459567870026],
     [132.98164627363735, 46.38576532847949],
     [301.0336906326895, 98.16046448916306],
     [238.25686790036065, 62.56535881619311],
     [227.2547443287154, 56.30924933427718],
     [209.13359962247614, 46.817221154818526],
     [203.9561297064078, 43.5813024572758]]
rdst = \
    [[10.822125594094452, 1.42189132706374],
     [21.177065426231174, 1.5297552836484982],
     [25.275895776451954, 1.42189132706374],
     [36.062291434927694, 1.6376192402332563],
     [40.376849698318004, 1.42189132706374],
     [11.900765159942026, -2.1376192402332563],
     [22.25570499207874, -2.1376192402332563],
     [26.785991168638553, -2.029755283648498],
     [37.033067044190524, -2.029755283648498],
     [41.67121717733509, -2.029755283648498]]

tform3_img = tf.ProjectiveTransform()
#tform3_img.estimate(np.array(rdst), np.array(rsrc))   # *2 required due to viewer size (640x480)
tform3_img.estimate(np.array(rdst) * 2, np.array(rsrc) * 2)  # *2 required due to viewer size (640x480)

def perspective_tform(x, y):
    p1, p2 = tform3_img((x,y))[0]
    return p2, p1

def draw_pt(img, x, y, color, sz=1):
    row, col = perspective_tform(x, y)
    if row >= 0 and row < img.shape[0] and \
                    col >= 0 and col < img.shape[1]:
        img[row-sz:row+sz, col-sz:col+sz] = color

def draw_path(img, path_x, path_y, color):
    for x, y in zip(path_x, path_y):
        draw_pt(img, x, y, color)

def calc_curvature(v_ego, angle_steers, angle_offset=0):
    slip_fator = 0.0014 # slip factor obtained from real data
    steer_ratio = 14.8  # from http://www.edmunds.com/acura/ilx/2016/road-test-specs/
    wheel_base = 2.85   # from http://www.edmunds.com/acura/ilx/2016/sedan/features-specs/

    angle_steers_rad = (angle_steers - angle_offset) #* deg_to_rad (Udacity data already in rads)
    curvature = angle_steers_rad/(steer_ratio * wheel_base * (1. + slip_fator * v_ego**2))
    return curvature

def calc_lookahead_offset(v_ego, angle_steers, d_lookahead, angle_offset=0):
    #*** this function returns the lateral offset given the steering angle, speed and the lookahead distance
    curvature = calc_curvature(v_ego, angle_steers, angle_offset)

    # clip is to avoid arcsin NaNs due to too sharp turns
    y_actual = d_lookahead * np.tan(np.arcsin(np.clip(d_lookahead * curvature, -0.999, 0.999))/2.)
    return y_actual, curvature

def draw_path_on(img, speed_ms, angle_steers, color=(0,0,255)):
    path_x = np.arange(0., 20.1, 0.25)
    path_y, _ = calc_lookahead_offset(speed_ms, angle_steers, path_x)
    draw_path(img, path_x, path_y, color)



    # x = np.zeros((1, 66, 200, 3))
    # y = np.zeros(1)
    # current_steering = -1
    # current_speed = 0
    # # cvbridge = CvBridge()
    # # bag = rosbag.Bag(bagpath)
    # # for topic, msg, t in bag.read_messages(topics=['/vehicle/steering_report', '/center_camera/image_color']):
    # #     if (topic == '/vehicle/steering_report'):
    # #         current_steering = msg.steering_wheel_angle
    # #         current_speed = msg.speed
    # #
    # #     if (current_steering != -1):
    # #         if (topic == '/center_camera/image_color'):
    # #             img = cvbridge.imgmsg_to_cv2(msg, "bgr8")
    # #             img_viewer = cv2.resize(img, (320, 240))
    # #             x[0,:,:,:] = cv2.resize(img, (200, 66))
    # #             y = model.predict(x, batch_size=1)
    # #
    # #             draw_path_on(img_viewer, current_speed, current_steering)
    # #             draw_path_on(img_viewer, current_speed, y[0])
    # #
    # #             cv2.imshow('Udacity challenge 2 - viewer', img)
    # #             key = cv2.waitKey(30)
    # #
    # #             if key == ord('q'):
    # #                 break
    # #
    # #             print "Steering angle: {} / Predicted: {}".format(current_steering, y[0])
    #
    # cv2.destroyAllWindows()

################################################################################
# Simple question yes/no, copied from somewhere
################################################################################
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
