import torch

from transformers import pipeline, AutoTokenizer

from src.utils import system_prompt_1, system_prompt_2


def parse_output(outputs: str) -> str:
    out = outputs[0]["generated_text"][-1]["content"]

    print("--> Output from model:")
    print(out)

    blocks = out.split('```')
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
from cga.client.cloudgripper_client import GripperRobot

token = os.environ['CLOUDGRIPPER_TOKEN']
robot = GripperRobot('robot2', token)
"""

    namespace = {}
    exec(setup_code, namespace)

    # print("--> Executing code block:")
    # print(code)

    exec(code, namespace)

if __name__ == "__main__":
    model_id = "meta-llama/Llama-3.2-3B-Instruct"
    model_id = "google/gemma-3-4b-it"


    tokenizer = AutoTokenizer.from_pretrained(model_id)
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        return_full_text=True,
    )

    messages = [
        {"role": "system", "content": system_prompt_2},
        # {"role": "user", "content": "Move to position X: 0.2, Y: 0.5, Z: 1 and close the gripper."},
        # {"role": "user", "content": "Move to the center of the box, then move to (0.3, 1, 0.8), wait for 2 seconds, and then open the gripper."},
        # {"role": "user", "content": "Move to the center of the box, then move in the plane forming a square"},
        {"role": "user", "content": "Move along a pentagon starting at (0.2, 0.2) with a side length of 0.2"},
        # {"role": "user", "content": "Follow the path (0.2, 0.2), (0.8, 0.2), (0.8, 0.8), (0.5, 0.5)"},
        # {"role": "user", "content": "Move in the plane forming a square with vertices at (0.2, 0.2), (0.8, 0.2), (0.8, 0.8), (0.2, 0.8)"},
        ]

    outputs = pipe(
        messages,
        max_new_tokens=2048,
        temperature=0.2,
        top_p=0.3,
        repetition_penalty=1.2,
        do_sample=True,
    )

    code = parse_output(outputs)
    run_code(code)