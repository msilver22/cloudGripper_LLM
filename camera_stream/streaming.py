import os
import cv2 as cv

from dotenv import load_dotenv
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client.cloudgripper_client import GripperRobot

load_dotenv()
robot = GripperRobot(os.environ['ROBOT_NAME'], os.environ['CLOUD_GRIPPER_TOKEN'])

cv.namedWindow("Bottom camera stream", cv.WINDOW_NORMAL)
cv.namedWindow("Top camera stream", cv.WINDOW_NORMAL)
cv.namedWindow("HSV Sliders", cv.WINDOW_NORMAL)

# Initial HSV values
hsv_min = [0, 184, 95]
hsv_max = [180, 255, 165]

# Trackbar callback (does nothing, required by OpenCV)
def nothing(x):
    pass

# Create trackbars for HSV min and max
cv.createTrackbar('H Min', 'HSV Sliders', hsv_min[0], 180, nothing)
cv.createTrackbar('S Min', 'HSV Sliders', hsv_min[1], 255, nothing)
cv.createTrackbar('V Min', 'HSV Sliders', hsv_min[2], 255, nothing)
cv.createTrackbar('H Max', 'HSV Sliders', hsv_max[0], 180, nothing)
cv.createTrackbar('S Max', 'HSV Sliders', hsv_max[1], 255, nothing)
cv.createTrackbar('V Max', 'HSV Sliders', hsv_max[2], 255, nothing)

while True:
    image_top, _ = robot.getImageTop()
    image_bottom, _ = robot.getImageBase()
    
    # Workspace rectangle coordinates for cropping
    origin = (155, 40)
    length_x = 405
    length_z = 420
    
    image_bottom = cv.rectangle(
        image_bottom,
        origin,
        (origin[0] + length_x, origin[1] + length_z),
        (0, 255, 0),
        2
    )

    hsv = cv.cvtColor(image_bottom, cv.COLOR_BGR2HSV)
    
    # Read trackbar positions
    h_min = cv.getTrackbarPos('H Min', 'HSV Sliders')
    s_min = cv.getTrackbarPos('S Min', 'HSV Sliders')
    v_min = cv.getTrackbarPos('V Min', 'HSV Sliders')
    h_max = cv.getTrackbarPos('H Max', 'HSV Sliders')
    s_max = cv.getTrackbarPos('S Max', 'HSV Sliders')
    v_max = cv.getTrackbarPos('V Max', 'HSV Sliders')
    
    hsv_min = (h_min, s_min, v_min)
    hsv_max = (h_max, s_max, v_max)
    
    # Optional: show mask for current HSV selection
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    cv.imshow("HSV Mask", mask)
    
    cv.imshow("Bottom camera stream", image_bottom)
    cv.imshow("Top camera stream", image_top)

    if cv.waitKey(10) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()