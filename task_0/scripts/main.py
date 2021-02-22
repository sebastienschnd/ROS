#!/usr/bin/env python
import rospy

import roslaunch

def start_task():
	rospy.loginfo("starting...")

	package = "task_0"
	executable = "script_2.py"
	node = roslaunch.core.Node(package, executable, args='_param1:=5')

	launch = roslaunch.scriptapi.ROSLaunch()
	launch.start()

	script = launch.launch(node)
	print script.is_alive()

def main():
	rospy.init_node('main_node')
	start_task()
	rospy.spin()

if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass