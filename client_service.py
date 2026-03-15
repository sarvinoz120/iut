import rospy
from my_robotics_pkg import AddTwoInts

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy(
            'add_two_ints', AddTwoInts)
        
        resp = add_two_ints(x, y)
        return resp.sum
        
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

if __name__ == "__main__":
    rospy.init_node('add_two_ints_client')
    result = add_two_ints_client(3, 7)
    rospy.loginfo(f"3 + 7 = {result}")