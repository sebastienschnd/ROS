#!/usr/bin/env/python

from __future__ import print_function

# Import ROS libraries and messages
import rospy
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError

import glob
import time

# Initialize the CVBridge class
bridge = CvBridge()


def vision_device_server():
    # Start the device node
    rospy.init_node("vision_device", anonymous=True)
    print("Starting vision_device_server")

    # Instantiate publisher
    _rate = 10
    rate = rospy.Rate(_rate)
    pub = rospy.Publisher('/device_topic', Image, queue_size=1000024)

    send_image = 'OK'
    # List of images
    filenames = [img for img in glob.glob("/tmp/images/*.jpg")]
    filenames.sort()

    while not rospy.is_shutdown():
        if send_image == 'OK':
            for img in filenames:
                # Load and convert first image
                cv_img = cv2.imread(img)
                print('Image %s is loaded' % img)
                img_msg = bridge.cv2_to_imgmsg(cv_img, "passthrough")
                time.sleep(3) # !!!!!!!!!
                print('Image has been converted by bridge')
                pub.publish(img_msg)
                time.sleep(10) # before loading another image
            
            # images should be sent once
            send_image = 'KO'
         
if __name__ == "__main__":
    try:
        vision_device_server()
    except rospy.ROSInterruptException:
        pass
