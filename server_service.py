#!/usr/bin/env python3
import rospy
from my_robotics_pkg import AddTwoInts

def handle_add_two_ints(req):
    result = req.a + req.b
    rospy.loginfo(f"Returning [{req.a} + {req.b} = {result}]")
    return AddTwoIntsResponse(result)

def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    
    # Advertise the service
    s = rospy.Service('add_two_ints', AddTwoInts,
                       handle_add_two_ints)
    rospy.loginfo("Ready to add two ints.")
    rospy.spin()  # Keep node alive

if __name__ == "__main__":
    add_two_ints_server()