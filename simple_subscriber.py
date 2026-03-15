#!/usr/bin/env python3
# simple_subscriber.py

import rospy
from std_msgs.msg import String

def callback(message):
    """This function is called every time a message arrives on the topic."""
    rospy.loginfo(f"Received: {message.data}")

def subscriber_node():
    rospy.init_node('simple_subscriber', anonymous=False)

    # Create a subscriber
    # Arguments: topic_name, message_type, callback_function
    rospy.Subscriber('/my_topic', String, callback)

    rospy.loginfo("Subscriber node started! Waiting for messages...")

    # Keep the node alive — hands control to ROS
    rospy.spin()

if __name__ == '__main__':
    try:
        subscriber_node()
    except rospy.ROSInterruptException:
        pass