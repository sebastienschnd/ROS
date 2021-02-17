#!/usr/bin/env python2
import rospy
from std_msgs.msg import String
from vision_getter_v1.msg import VisionDetectedObjects

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard objet: %s, confidence: %i, distance: %i", data.label, data.confidence, data.distance)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("custom_chatter", VisionDetectedObjects, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
