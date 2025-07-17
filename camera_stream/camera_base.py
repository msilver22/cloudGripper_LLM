import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client.cloudgripper_client import GripperRobot
import time
import cv2

# Get the CloudGripper API token from environment variables
token = os.environ['CLOUDGRIPPER_TOKEN']

# Create a GripperRobot instance
robotName = 'robot2'
robot = GripperRobot(robotName, token)

while True:
    image, timestamp = robot.getImageBase()
    cv2.imshow("Cloudgripper top camera stream", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break