#!/usr/bin/env/python

from __future__ import print_function

# Import service 
from vision_getter_v3.srv import ImageGetter, ImageGetterResponse

# Import ROS libraries and messages
import rospy
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError

def handle_send_image(req):
    # Initialize the CvBridge class
    bridge = CvBridge()
    # Load the image from /tmp/image.jpg
    print("Loading image from /tmp/image.jpg")
    cv_img = cv2.imread("/tmp/image.jpg")
    # Image conversion
    try:
        print ("Start image conversion with CvBridge")
        img_msg = bridge.cv2_to_imgmsg(cv_img)
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}", format(e))

    return(ImageGetterResponse(img_msg))


def vision_device_server():
    rospy.init_node('vision_device')
    s = rospy.Service('send_image', ImageGetter, handle_send_image)
    print("Ready to send image")
    rospy.spin()

if __name__ == "__main__":
    vision_device_server()