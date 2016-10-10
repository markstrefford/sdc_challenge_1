import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from dbw_mkz_msgs.msg import SteeringReport
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from Queue import Queue
import h5py

class DataParser:

    def __init__(self):

        self.center_bridge = CvBridge()
        self.left_bridge = CvBridge()
        self.right_bridge = CvBridge()
        self.center_image_sub = rospy.Subscriber("/center_camera/image_color",Image,self.callback1)
        self.left_image_sub = rospy.Subscriber("/left_camera/image_color",Image,self.callback2)
        self.right_image_sub = rospy.Subscriber("/right_camera/image_color",Image,self.callback3)
        self.steering_wheel_angle_sub = rospy.Subscriber('/vehicle/steering_report', SteeringReport, self.steering_callback)
        self.center_camera_container = Queue(maxsize=0)
        self.left_camera_container = Queue(maxsize=0)
        self.right_camera_container = Queue(maxsize=0)
        self.steering_wheel_angle_container = Queue(maxsize=0)

    # DRY principle here. One callback to handle all the cameras
    def callback(self,camera_container,camera_bridge,data, image_window_number=str(1)):
        try:
            cv_image = camera_bridge.imgmsg_to_cv2(data, "bgr8")
            camera_container.put(cv_image)
        except CvBridgeError as e:
            print(e)


        #cv2.imshow("Image window " + image_window_number, cv_image)
        #cv2.waitKey(3)

    def steering_callback(self,Steering_report_msg):
        #rospy.loginfo(' I heard Steering Report with steering = %f' %Steering_report_msg.steering_wheel_angle)
        self.steering_wheel_angle_container.put(Steering_report_msg.steering_wheel_angle)

    def datawriter(self,file_handle):
        if not self.center_camera_container.empty():
            center_camera = self.center_camera_container.get()
            self.center_camera_container.task_done()
            #print 'center_camera',center_camera.shape
        if not self.right_camera_container.empty():
            right_camera = self.right_camera_container.get()
            self.right_camera_container.task_done()
            #print 'right_camera',right_camera.shape
        if not self.left_camera_container.empty():
            left_camera = self.left_camera_container.get()
            self.left_camera_container.task_done()
            #print 'left_camera',left_camera.shape
        if not self.steering_wheel_angle_container.empty():
            steering_wheel_angle = self.steering_wheel_angle_container.get()
            self.steering_wheel_angle_container.task_done()
            #print 'steering_wheel_angle = ',steering_wheel_angle

if __name__ == '__main__':
    rospy.init_node('data_converter', anonymous=True)
    try:
        converter = DataParser()
        write_rate = 5 # ms
        rate = rospy.Rate(1000/write_rate)
        with h5py.File('udacity_part1.hdf5') as h5_file:
            center_camera_data = h5_file.create_dataset("center_camera",(1,460,680,3), maxshape=(none,460,680,3))
            right_camera_data = h5_file.create_dataset("right_camera",(1,460,680,3), maxshape=(none,460,680,3))
            left_camera_data = h5_file.create_dataset("left_camera",(1,460,680,3), maxshape=(none,460,680,3))
            time_data = h5_file.create_dataset("time",(1,1),, maxshape=(none,1))
            steering_wheel_angle_data = h5_file.create_dataset("steering_wheel_angle",(1,1),, maxshape=(none,1))
            while not rospy.is_shutdown():
                converter.datawriter(h5_file)
                rate.sleep()
    finally:
        #h5_file.close()
        print "closing node"
