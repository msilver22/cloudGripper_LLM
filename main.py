from groq import Groq
from src.utils import base_prompt
from dotenv import load_dotenv
import os

def parse_output(outputs: str) -> str:

    blocks = outputs.split('```')
    if len(blocks) != 3:
        raise ValueError(f"Output does not contain the required delimiters.")

    code = blocks[1]
    if not code.startswith("python"):
        raise ValueError(f"Output code block does not start with 'python'.")
    
    code = code.removeprefix("python").strip()

    return code

def run_code(code: str):
    setup_code = """
import os
import time
from client.cloudgripper_client import GripperRobot
from dotenv import load_dotenv
import os

load_dotenv()
token = os.environ['CLOUDGRIPPER_TOKEN']
robot = GripperRobot('robot2', token)
"""

    namespace = {}
    exec(setup_code, namespace)

    # print("--> Executing code block:")
    # print(code)

    exec(code, namespace)


def main(): 

    load_dotenv()
    groq_key = os.environ.get('GROQ_API_KEY')
    client = Groq(api_key=groq_key)

    model_name = "llama-3.3-70b-versatile"
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": base_prompt},
            {
                "role": "user",
                "content": "Move to position X: 0.2, Y: 0.5, Z: 1, open and close the gripper."
                #"content": "Move to (0.3,0.6), open the gripper, touch the ground, and close the gripper."
                #"content": "Move along a circle with 20 points."
                #"content": "Move along a regular penthagon, starting at (0.2,0.2). Then open and close the gripper."
            }
        ]
    )
    outputs = completion.choices[0].message.content
    print("--> Model response:")
    print(outputs)

    # Parsing the output to extract the code block
    code = parse_output(outputs)
    run_code(code)











if __name__ == "__main__":
    main()