#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import math

x_pos = 0.000
y_pos = 0.000
theta_pos = 0.000
lin_vel = 0.000
ang_vel = 0.000

#Pose callback
def pose_callback(data):
    global x_pos, y_pos, theta_pos, lin_vel, ang_vel
    x_pos = float('%.3f'%(data.x))
    y_pos = float('%.3f'%(data.y))
    theta_pos = float('%.3f'%(data.theta))
    lin_vel = float('%.3f'%(data.linear_velocity))
    ang_vel = float('%.3f'%(data.angular_velocity))

if __name__ == '__main__':
    try:
        #Set up publisher and subscriber topics
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('turtle1/pose', Pose, pose_callback)

        rospy.init_node('mines_logo') #initialize node
        
        #Variables to use for proportional control (closed-loop control)
        tolerance = 0.1
        gain = 1

        #Checkpoints
        checkpoints = [(4.544,6.736),(4.544,4.736),(5.044,4.736),(5.044,4.236),(3.544,4.236),(3.544,4.736),
                        (4.044,4.736),(4.044,6.736),(3.544,6.736),(3.544,7.236),(4.544,7.236),(5.644,6.044),
                        (6.544,7.236),(7.544,7.236),(7.544,6.736),(7.044,6.736),(7.044,4.736),(7.544,4.736),
                        (7.544,4.236),(6.044,4.236),(6.044,4.736),(6.544,4.736),(6.544,6.736),(5.544,5.544)]

        #Go through each checkpoint
        for i in range(len(checkpoints)):
            pose_cmd = Twist() #Set up Pose message
            x_desired = checkpoints[i][0]
            y_desired = checkpoints[i][1]
            error = math.sqrt((abs(x_pos-x_desired))**2 + (abs(y_pos-y_desired))**2)
            while(error > tolerance and not rospy.is_shutdown()):
                pose_cmd.linear.x = gain * error
                #Set x velocity
                if(x_pos > x_desired):
                    pose_cmd.linear.x = -gain * error
                #Set y velocity
                pose_cmd.linear.y = gain * error
                if(y_pos > y_desired):
                    pose_cmd.linear.y = -gain * error
                error = math.sqrt((abs(x_pos-x_desired))**2 + (abs(y_pos-y_desired))**2) #Update error   
                pub.publish(pose_cmd) #Publish

    except rospy.ROSInterruptException:
        pass
