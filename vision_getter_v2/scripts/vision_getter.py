#!/usr/bin/env python

from __future__ import print_function

# Import service
from vision_getter_v2.srv import *

# Import ROS libraries and messages
import rospy
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError

def vision_device_client():
    rospy.wait_for_service('send_image')
    try:
        send_image = rospy.ServiceProxy('send_image', ImageGetter)
        resp1 = send_image()
        return resp1.img 
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":
    rospy.init_node('vision_getter')
    # Initialize the CvBridge class
    bridge = CvBridge()
    # Requestion for an image
    print("Request for an image")
    img_msg = vision_device_client()
    #print(img_msg)
    # Image conversion
    cv_img = bridge.imgmsg_to_cv2(img_msg, desired_encoding='passthrough')
    #print(cv_img)
    # Show the converted image
    cv2.imshow("Image Window", cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
