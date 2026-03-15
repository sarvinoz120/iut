#!/usr/bin/env python3
# simple_publisher.py

import rospy
from std_msgs.msg import String

def publisher_node():
    # Initialize the node with a name
    rospy.init_node('simple_publisher', anonymous=False)

    # Create a publisher
    # Arguments: topic_name, message_type, queue_size
    pub = rospy.Publisher('/my_topic', String, queue_size=10)

    # Set the publish rate (10 Hz)
    rate = rospy.Rate(10)

    rospy.loginfo("Publisher node started!")

    while not rospy.is_shutdown():
        message = String()
        message.data = f"Hello, This is IUT CD class! Time: {rospy.get_time():.2f}"

        pub.publish(message)
        rospy.loginfo(f"Published: {message.data}")

        rate.sleep()  # Sleep to maintain 10 Hz rate

if __name__ == '__main__':
    try:
        publisher_node()
    except rospy.ROSInterruptException:
        pass