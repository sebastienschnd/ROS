#!/usr/bin/env python2.7
# Import ROS libraries and messages
import rospy
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError

# Print "Hello!" to terminal
print "Hello!"

# Initialize the ROS Node named "vision_getter_node", allow multiple nodes to be run with this name
rospy.init_node('vision_getter_node', anonymous=True)

# Print "Hello ROS!" to the Terminal and to ROS Log file located in ~/.ros/log/logbash/*.log
rospy.loginfo("Hello ROS!")

# Initialize the CvBridge class
bridge = CvBridge()

# Define a function to show Image in an OpenCv Window
def show_image(img):
    cv2.imshow("Image Window", img)
    cv2.waitKey(3)

# Define a callback for the Image message
def image_callback(img_msg):
    # log some infos about the image topic
    print "enter the callback"
    rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        print "enter the try"
        cv_image = bridge.imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
    except CvBridgeError, e:
        print "enter the exception"
        rospy.logerr("CvBridge Error: {0}", format(e))
    
    # Show the converted image
    show_image(cv_image)

# Initialize a subscriber to the "/videofile/videofile_image_view/output" topic with the function "image_callback" as a callback
sub_image = rospy.Subscriber("/videofile/videofile_image_view/output", Image, image_callback)

# Initialize an OpenCv window named "Image window"
# cv2.namedWindow("Image Window")

# Loop to keep the program from shutting down unless ROS is shutdown, or CTRL-C is pressed
while not rospy.is_shutdown():
    rospy.spin()