#!/usr/bin/env python

from __future__ import print_function

# Import service
from vision_getter_v3.srv import *

# Import ROS libraries and messages
import rospy
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
import numpy as np
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
    # initialize the node
    rospy.init_node('vision_getter')

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
    
    # Request for an image
    print("Request for an image")
    img_msg = vision_device_client()
    
    # Image conversion
    cv_img = bridge.imgmsg_to_cv2(img_msg, desired_encoding="passthrough")
    cv_img = cv2.resize(cv_img, None, fx=0.4, fy=0.4)
    height, width, channels = cv_img.shape

    # Detecting objets inside image
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

    # Show the converted image
    cv2.imshow("Image window", cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

    
