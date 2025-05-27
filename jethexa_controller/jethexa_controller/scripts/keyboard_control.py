#!/usr/bin/env python3
# coding: utf-8

import sys
import rospy
import curses
import math
from geometry_msgs.msg import Twist
from jethexa_controller_interfaces.msg import Traveling
from jethexa_controller_interfaces.srv import SetPose1, SetPose1Request

def main(stdscr):
    msg = Twist()
    tmsg = Traveling()
    last_keycode = ord('.')
    curses.curs_set(0)
    stdscr.addstr(0, 0, "Enter : Stand         |  Space : Stop")
    stdscr.addstr(1, 0, "W / ↑ : Move Forward  |  S / ↓ : Move Backward")
    stdscr.addstr(2, 0, "A     : Move Left     |  D     : Move Right")
    stdscr.addstr(3, 0, "←     : Trun Left     |  →     : Turn Right")
    stdscr.addstr(5, 0, ">>>          <<<")
    
    rospy.wait_for_service('jethexa_controller/set_pose_1')
    set_pose_client = rospy.ServiceProxy('jethexa_controller/set_pose_1', SetPose1)
    
    while not rospy.is_shutdown():
        keycode = stdscr.getch()
        if keycode == ord('\n'):
            stdscr.addstr(1, 0, "Stand")
            tmsg.gait = -2 #Merujuk pada jet_con_main.py def set_traveling_cb()
            tmsg.time = 1.0
            traveling_pub.publish(tmsg)
        if last_keycode == keycode:
            continue
        last_keycode = keycode

        if keycode == curses.KEY_UP or keycode == ord('w'):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Move Forward <<<")
            # tmsg = Traveling()
            # tmsg.gait = 1
            # tmsg.time = 1.0
            # tmsg.height = 50.0
            # tmsg.steps = 5
            msg.linear.x, msg.linear.y = 0.08, 0.0
            msg.angular.z = 0.0
            cmd_vel_pub.publish(msg)
            # traveling_pub.publish(tmsg)
            
        elif keycode == ord('x'):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Move Diagonal Left <<<")
            tmsg.gait = 1
            tmsg.stride = 40.0
            tmsg.time = 1.0
            tmsg.height = 50.0
            tmsg.steps = 10
            tmsg.direction = math.radians(45)
            tmsg.rotation = 0.0
            tmsg.interrupt = True
            tmsg.relative_height = False
            traveling_pub.publish(tmsg)
            
        elif keycode == ord('z'):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Move Diagonal Right<<<")
            tmsg.gait = 1
            tmsg.stride = 40.0
            tmsg.time = 1.0
            tmsg.height = 50.0
            tmsg.steps = 10
            tmsg.direction = math.radians(315)
            tmsg.rotation = 0.0
            tmsg.interrupt = True
            tmsg.relative_height = False
            traveling_pub.publish(tmsg)
            
        elif keycode == ord('c'):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> DEFAULT_POSE <<<")
            try:
                req = SetPose1Request()
                req.pose = "DEFAULT_POSE"
                req.duration = 2.0
                req.interrupt = True
                res = set_pose_client(req)
                if res.result != 0:
                    rospy.logerr("Set pose failed: " + res.message)
            except rospy.ServiceException as e:
                rospy.logerr("Service call failed: %s" % e)

        elif keycode == curses.KEY_DOWN or keycode == ord('s'):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Move Backward <<<")
            msg.linear.x, msg.linear.y = -0.08, 0.0
            msg.angular.z = 0.0
            cmd_vel_pub.publish(msg)

        elif keycode == curses.KEY_LEFT:
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, "Turn Left")
            msg.linear.x, msg.linear.y = 0.0, 0.0
            msg.angular.z = 0.25
            cmd_vel_pub.publish(msg)

        elif keycode == curses.KEY_RIGHT:
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Turn Right <<<")
            msg.linear.x, msg.linear.y = 0.0, 0.0
            msg.angular.z = -0.25
            cmd_vel_pub.publish(msg)

        elif keycode == ord('a'):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Move Left <<<")
            msg.linear.x, msg.linear.y = 0.0, 0.05
            msg.angular.z = 0.0
            cmd_vel_pub.publish(msg)

        elif keycode == ord('d'):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Move Right <<<")
            msg.linear.x, msg.linear.y = 0.0, -0.05
            msg.angular.z = 0.0
            cmd_vel_pub.publish(msg)

        elif keycode == ord(' '):
            stdscr.addstr(5, 0, " "*40)
            stdscr.addstr(5, 0, ">>> Stop <<<")
            msg.linear.x, msg.linear.y = 0.0, 0.0
            msg.angular.z = 0.0
            cmd_vel_pub.publish(msg)

        else:
            pass

if __name__ == '__main__':
    try:
        rospy.init_node('keyboard_cotnrol_node')
        topic_prefix = rospy.get_param("~topic_prefix", "jethexa_controller")
        cmd_vel_pub = rospy.Publisher(topic_prefix + '/cmd_vel', Twist, queue_size=1)
        traveling_pub = rospy.Publisher(topic_prefix + '/traveling', Traveling, queue_size=1)
        curses.wrapper(main)
    except Exception as e:
        rospy.logerr(str(e))

