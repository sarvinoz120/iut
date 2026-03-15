#!/usr/bin/env python3
# robot_status_subscriber.py
import rospy
from my_robotics_pkg import RobotStatus

def callback(msg):
    rospy.loginfo("--- Robot Status Update ---")
    rospy.loginfo(f"  Robot:    {msg.robot_name}")
    rospy.loginfo(f"  Battery:  {msg.battery_level:.1f}%")
    rospy.loginfo(f"  Moving:   {msg.is_moving}")
    rospy.loginfo(f"  Error:    {msg.error_code}")

    if msg.battery_level < 20.0:
        rospy.logwarn("LOW BATTERY WARNING!")

def subscriber_node():
    rospy.init_node('robot_status_subscriber')
    rospy.Subscriber('/robot_status', RobotStatus, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        subscriber_node()
    except rospy.ROSInterruptException:
        pass