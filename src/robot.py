import time
import cv2 as cv
import numpy as np

from typing import Tuple
from client.cloudgripper_client import GripperRobot
from value_iteration import RobotPolicy

class RobotController(GripperRobot):
    
    def __init__(self, robot_name: str, token: str, origin: Tuple[int, int] = (40, 155), length_x: int = 405, length_y: int = 420):
        super().__init__(robot_name, token)
        
        # Workspace rectangle coordinates for cropping
        self.origin = origin
        self.length_x = length_x
        self.length_z = length_y
        self.policy_generator = RobotPolicy(N_rows=20, N_cols=20)

    def pick(self):
        self.gripper_open()
        self.move_z(0)
        time.sleep(2)
        self.gripper_close()
        self.move_z(1)

    def place(self):
        self.move_z(0)
        time.sleep(2)
        self.gripper_open()
        self.move_z(1)

    def go_to_cube(self):
        x, y = self.detect_cube()

        if x < 0 or y < 0:
            print("No cube detected.")
            return

        opt_policy = self.policy_generator.compute_optimal_solution(cube_center=(x, y))
        self.follow_policy(opt_policy)

    def detect_cube(self, img: np.ndarray, hsv_min: Tuple[int, int, int] = (0, 185, 0), hsv_max: Tuple[int, int, int] = (180, 255, 255)) -> Tuple[float, float]:
        # Crop the image to the defined rectangle
        origin_x, origin_y = self.origin
        cropped = img[origin_y:origin_y + self.length_z, origin_x:origin_x + self.length_x]

        # Extract a mask for the red cube in the image
        hsv = cv.cvtColor(cropped, cv.COLOR_BGR2HSV)
        masked_hsv = cv.inRange(hsv, np.array(hsv_min), np.array(hsv_max))
        masked_opened = cv.morphologyEx(masked_hsv, cv.MORPH_OPEN, np.ones((5, 5), np.uint8))
        contours, _ = cv.findContours(masked_opened, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if not contours:
            return (-1, -1)  # No cube found

        # Find the largest contour
        if contours:
            largest_contour = max(contours, key=cv.contourArea)
            largest_mask = np.zeros_like(masked_opened)
            cv.drawContours(largest_mask, [largest_contour], -1, 255, thickness=cv.FILLED)
            masked_opened = largest_mask

        # Find the center of the largest contour
        non_zero = np.argwhere(masked_opened > 0)
        avg_y, avg_x = np.mean(non_zero, axis=0)

        # Normalize the coordinates w.r.t. the cropped image size
        avg_x = avg_x / self.length_x
        avg_y = avg_y / self.length_z

        return (avg_x, avg_y)
    
    def follow_policy(self, policy):
        end_reached = False
        r, c = self.reset()

        while not end_reached:
            action = policy[r, c]
            dr, dc = self.actions[action]
            
            # we move the real robot
            if action == 0:
                self.step_left()
            elif action == 1:
                self.step_right()
            elif action == 2:
                self.step_forward()
            elif action == 3:
                self.step_backward()
            elif action == 4:
                end_reached = True  # stay in the same position

            new_r, new_c = r + dr, c + dc

            # Check boundaries
            r = max(0, min(new_r, self.N_rows - 1))
            c = max(0, min(new_c, self.N_cols - 1))