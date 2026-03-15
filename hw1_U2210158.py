#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced TurtleSim Digit Drawing — Homework #1
Capstone Design [202601-ICE/CSE4020]

Draws any four digits simultaneously in the turtlesim window.
Defaults to student ID: 0, 1, 5, 8.

The implementation uses a class-based structure for better organization,
implements all digits (0-9) with curved strokes, and ensures synchronized start.

Usage:
    1. In terminal 1:  roscore
    2. In terminal 2:  rosrun turtlesim turtlesim_node
    3. In terminal 3:  python3 hw1_0158.py [DIGITS]
       (Example: python3 hw1_0158.py 2024)
"""

import rospy
import threading
import math
import sys
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn, TeleportAbsolute, SetPen

# ═══════════════════════════════════════════════════════════════════
#  Configuration
# ═══════════════════════════════════════════════════════════════════

RATE_HZ = 100
DEFAULT_SPEED = 1.5
PEN_WIDTH = 4
PEN_COLOR = (220, 220, 255)  # Light blue-white

# Viewport constants
CANVAS_SIZE = 11.08
ZONES = 4
ZONE_WIDTH = CANVAS_SIZE / ZONES
CENTER_Y = CANVAS_SIZE / 2.0

# ═══════════════════════════════════════════════════════════════════
#  TurtleDigitDrawer Class
# ═══════════════════════════════════════════════════════════════════

class TurtleDigitDrawer:
    def __init__(self, turtle_name, digit, cx, cy, barrier):
        self.name = turtle_name
        self.digit = int(digit)
        self.cx = cx
        self.cy = cy
        self.barrier = barrier
        
        self.pub = rospy.Publisher('/{}/cmd_vel'.format(self.name), Twist, queue_size=10)
        self.rate = rospy.Rate(RATE_HZ)
        
        # Service proxies
        self.teleport_proxy = rospy.ServiceProxy('/{}/teleport_absolute'.format(self.name), TeleportAbsolute)
        self.set_pen_proxy = rospy.ServiceProxy('/{}/set_pen'.format(self.name), SetPen)

    # --- Helpers ---
    
    def teleport(self, x, y, theta):
        self.teleport_proxy(x, y, theta)

    def set_pen(self, r=255, g=255, b=255, width=PEN_WIDTH, off=False):
        self.set_pen_proxy(r, g, b, width, int(off))

    def pen_up(self):
        self.set_pen(off=True)

    def pen_down(self):
        self.set_pen(r=PEN_COLOR[0], g=PEN_COLOR[1], b=PEN_COLOR[2], width=PEN_WIDTH, off=False)

    def _publish_for(self, twist, duration):
        steps = int(duration * RATE_HZ)
        for _ in range(steps):
            if rospy.is_shutdown(): return
            self.pub.publish(twist)
            self.rate.sleep()
        self.pub.publish(Twist())
        self.rate.sleep()

    def move_forward(self, distance, speed=DEFAULT_SPEED):
        twist = Twist()
        twist.linear.x = speed
        duration = abs(distance) / speed
        self._publish_for(twist, duration)

    def draw_arc(self, radius, sweep_angle, speed=DEFAULT_SPEED):
        angular_vel = speed / radius
        if sweep_angle < 0: angular_vel = -angular_vel
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = angular_vel
        duration = abs(sweep_angle) * radius / speed
        self._publish_for(twist, duration)

    # --- Digit Rendering Methods ---

    def draw_0(self):
        r, s = 0.75, 1.4
        self.pen_up()
        self.teleport(self.cx - r, self.cy + s/2.0, math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(r, -math.pi)
        self.move_forward(s)
        self.draw_arc(r, -math.pi)
        self.move_forward(s)

    def draw_1(self):
        h = 1.45
        self.pen_up()
        self.teleport(self.cx - 0.35, self.cy + h - 0.35, math.pi/5.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(1.5, math.pi/7.0)
        self.pen_up()
        self.teleport(self.cx, self.cy + h, -math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.move_forward(2*h)
        self.pen_up()
        self.teleport(self.cx - 0.35, self.cy - h, 0.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(4.0, 0.7/4.0)

    def draw_2(self):
        r = 0.7
        self.pen_up()
        self.teleport(self.cx - r, self.cy + 1.0, math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(r, -(math.pi + 0.5)) # Top curve
        # Straight line to bottom-left
        self.pen_up()
        self.teleport(self.cx + r, self.cy + 1.0 - r + 0.1, -2.5) # Approximate angle
        self.pen_down()
        self.move_forward(2.6)
        self.teleport(self.cx - r, self.cy - 1.4, 0.0)
        self.move_forward(2*r)

    def draw_3(self):
        r = 0.7
        self.pen_up()
        self.teleport(self.cx - r, self.cy + 0.7, math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(r, -1.5 * math.pi)
        self.pen_up()
        self.teleport(self.cx - 0.1, self.cy - 0.1, 0.5)
        self.pen_down()
        self.draw_arc(0.8, -1.6 * math.pi)

    def draw_4(self):
        w, h = 0.7, 1.4
        self.pen_up()
        self.teleport(self.cx - w, self.cy + h, -math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.move_forward(h)
        self.teleport(self.cx - w, self.cy, 0.0)
        self.move_forward(2*w)
        self.pen_up()
        self.teleport(self.cx + w/2.0, self.cy + h, -math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.move_forward(2*h)

    def draw_5(self):
        h, w = 1.45, 0.7
        self.pen_up()
        self.teleport(self.cx + w, self.cy + h, math.pi)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(10.0, 2*w/10.0)
        self.pen_up()
        self.teleport(self.cx - w, self.cy + h, -math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.move_forward(h)
        self.pen_up()
        self.teleport(self.cx - w, self.cy, 0.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(0.72, -(math.pi * 0.95))

    def draw_6(self):
        r = 0.7
        self.pen_up()
        self.teleport(self.cx + r, self.cy + 1.4, math.pi)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(2.0, math.pi/3.0)
        self.draw_arc(r, 2*math.pi) # Circle at bottom
        self.pen_up()
        self.teleport(self.cx - r, self.cy + 0.5, math.pi/2.0)
        self.pen_down()
        self.move_forward(0.7)

    def draw_7(self):
        w, h = 0.7, 1.4
        self.pen_up()
        self.teleport(self.cx - w, self.cy + h, 0.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.move_forward(2*w)
        self.teleport(self.cx + w, self.cy + h, -math.pi/1.3)
        self.move_forward(2.9)

    def draw_8(self):
        r_u, r_l = 0.62, 0.75
        self.pen_up()
        self.teleport(self.cx - r_u, self.cy + r_u, math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(r_u, -2*math.pi)
        self.pen_up()
        self.teleport(self.cx - r_l, self.cy - r_l, -math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(r_l, 2*math.pi)

    def draw_9(self):
        r = 0.7
        self.pen_up()
        self.teleport(self.cx + r, self.cy + 0.7, -math.pi/2.0)
        rospy.sleep(0.1)
        self.pen_down()
        self.draw_arc(r, 2*math.pi) # Circle at top
        self.pen_up()
        self.teleport(self.cx + r, self.cy + 0.7, -math.pi/2.0)
        self.pen_down()
        self.move_forward(2.1)

    def run(self):
        rospy.loginfo("Turtle %s ready. Waiting for barrier...", self.name)
        self.barrier.wait()
        rospy.loginfo("Turtle %s starting drawing %d", self.name, self.digit)
        
        draw_map = {
            0: self.draw_0, 1: self.draw_1, 2: self.draw_2, 3: self.draw_3, 4: self.draw_4,
            5: self.draw_5, 6: self.draw_6, 7: self.draw_7, 8: self.draw_8, 9: self.draw_9
        }
        
        func = draw_map.get(self.digit)
        if func:
            func()
        else:
            rospy.logwarn("Digit %d not implemented", self.digit)

# ═══════════════════════════════════════════════════════════════════
#  Main Loop
# ═══════════════════════════════════════════════════════════════════

def main():
    rospy.init_node('digit_drawer_pro', anonymous=False)
    
    # Parse digits from command line or use default
    digits_input = sys.argv[1] if len(sys.argv) > 1 else "0158"
    digits = [int(d) for d in digits_input[:4]]
    
    rospy.loginfo("Initializing Digit Drawer with ID: %s", "".join(map(str, digits)))
    
    # Setup services
    rospy.wait_for_service('/spawn')
    spawn_service = rospy.ServiceProxy('/spawn', Spawn)
    
    turtle_names = ['turtle1', 'turtle2', 'turtle3', 'turtle4']
    
    # Spawn missing turtles
    for i in range(1, 4):
        try:
            spawn_service(5.5, 5.5, 0.0, turtle_names[i])
        except rospy.ServiceException:
            pass # Already exists
            
    # Position turtles in zones
    centers_x = [(i + 0.5) * ZONE_WIDTH for i in range(ZONES)]
    
    barrier = threading.Barrier(4)
    threads = []
    
    for i in range(4):
        name = turtle_names[i]
        digit = digits[i]
        cx = centers_x[i]
        
        drawer = TurtleDigitDrawer(name, digit, cx, CENTER_Y, barrier)
        t = threading.Thread(target=drawer.run)
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
        
    rospy.loginfo("All digits drawn successfully.")
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
