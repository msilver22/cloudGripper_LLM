import os
from client.cloudgripper_client import GripperRobot

token = os.environ['CLOUDGRIPPER_TOKEN']
robot = GripperRobot('robot2', token)

import time
robot.move_xy(0.2, 0.2)
time.sleep(2)
robot.move_xy(0.2, 0.8)
time.sleep(2)
robot.move_xy(0.8, 0.8)
time.sleep(2)
robot.move_xy(0.8, 0.2)
