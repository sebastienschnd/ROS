#!/usr/bin/env python
# licence removed from brevety
import rospy
from std_msgs.msg import String
from vision_getter_v1.msg import VisionDetectedObjects

def talker():
    pub = rospy.Publisher('custom_chatter', VisionDetectedObjects, queue_size=10)
    rospy.init_node('custom_talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg = VisionDetectedObjects()
    msg.label = "Green Lantern"
    msg.confidence = 50
    msg.distance = 110
    while not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
