#!/usr/bin/env python

from __future__ import print_function

# Import service
from vision_getter_v4.srv import *

# Import ROS libraries and messages
import rospy
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
import numpy as np 
from cv_bridge import CvBridge, CvBridgeError
import roslaunch

# Initialize the CvBridge class
bridge = CvBridge()

# Define a function to show Image in an OpenCv Window
def show_image(img):
    cv2.imshow("Image Window", img)
    cv2.waitKey(2000)
    #cv2.destroyAllWindows()

def image_callback(img_msg):
    rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        print ("enter the try")
        cv_image = bridge.imgmsg_to_cv2(img_msg, desired_encoding="passthrough")
    except CvBridgeError, e:
        print ("enter the exception")
        rospy.logerr("CvBridge Error: {0}", format(e))
    
    # Show the converted image
    show_image(cv_image)

#def vision_device_client(tempo):
def vision_device_client():
    pub = rospy.init_node('vision_getter', anonymous=True)
    rospy.Subscriber("/device_topic", Image, image_callback)
    rospy.spin()

if __name__ == "__main__":
    print("Start subscribing to related images topic")
    vision_device_client()
