from client.cloudgripper_client import GripperRobot
import time
import sys
import cv2
import os

# Get the CloudGripper API token from environment variables
token = os.environ['CLOUDGRIPPER_TOKEN']

# Create a GripperRobot instance
robotName = 'robot2'
robot = GripperRobot(robotName, token)

while True:
    image, timestamp = robot.getImageTop()
    cv2.imshow("Cloudgripper top camera stream", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break