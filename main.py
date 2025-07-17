import os
import time

from dotenv import load_dotenv
from src.model import ModelClient
from src.robot import RobotController

def run_code(code: str, robot: RobotController):
    # Add the robot instance to the execution context, and some common modules to the namespace
    namespace = {"robot": robot, 'time': time}
    exec(code, namespace)

def main():
    # Create the LLM client
    model_client = ModelClient("llama-3.3-70b-versatile")

    # Create the CloudGripper controller
    load_dotenv()
    robot = RobotController(os.environ['ROBOT_NAME'], os.environ['CLOUD_GRIPPER_TOKEN'])

    while True:
        user_input = input("Enter your command for the robot: ")
        if user_input.lower() == 'exit':
            break

        # Query the model with the user input
        outputs, code = model_client.query_model(user_input)
        
        print("--> Model response:")
        print(outputs)

        # Run the code in the robot's context
        run_code(code, robot)


if __name__ == "__main__":
    main()