#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def main():
    rospy.init_node('script_2', anonymous=True)
    param = rospy.get_param("~param1")
    rate = rospy.Rate(param)
    pub = rospy.Publisher('chatter', String, queue_size=10)
	
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass