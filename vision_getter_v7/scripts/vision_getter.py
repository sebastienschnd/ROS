#!/usr/bin/env python

from __future__ import print_function

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

# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


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

    cv_img = cv2.resize(cv_image, None, fx=0.4, fy=0.4)
    height, width, chanels = cv_img.shape 

    # Detecting objects inside image
    blob = cv2.dnn.blobFromImage(cv_img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(cv_img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(cv_img, label, (x, y + 30), font, 3, color, 3)
    
    # Show the converted original image
    #show_image(cv_image)

    # Show image with boxes
    show_image(cv_img)
#def vision_device_client(tempo):
def vision_device_client():
    pub = rospy.init_node('vision_getter', anonymous=True)
    rospy.Subscriber("/device_topic", Image, image_callback)
    rospy.spin()

if __name__ == "__main__":
    print("Start subscribing to related images topic")
    vision_device_client()
