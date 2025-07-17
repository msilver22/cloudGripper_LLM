import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client.cloudgripper_client import GripperRobot
import time
import cv2
from dotenv import load_dotenv
import os

load_dotenv()

# Get the CloudGripper API token from environment variables

token = os.environ['CLOUD_GRIPPER_TOKEN']

# Create a GripperRobot instance
robotName = os.environ['ROBOT_NAME']
robot = GripperRobot(robotName, token)

while True:
    image, timestamp = robot.getImageTop()
    cv2.imshow("Cloudgripper top camera stream", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break