
import os
from typing import Tuple
from groq import Groq
from dotenv import load_dotenv
from src.utils import base_prompt


class ModelClient():
    def __init__(self, model_name):    
        load_dotenv()
        groq_key = os.environ.get('GROQ_API_KEY')
        self.client = Groq(api_key=groq_key)
        self.model_name = model_name

    def query_model(self, user_input: str) -> Tuple[str, str]:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": base_prompt},
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        outputs = completion.choices[0].message.content
        code = self.parse_output(outputs)

        return outputs, code
    
    def parse_output(self, outputs: str) -> str:
        blocks = outputs.split('```')
        if len(blocks) != 3:
            raise ValueError(f"Output does not contain the required delimiters.")

        code = blocks[1]
        if not code.startswith("python"):
            raise ValueError(f"Output code block does not start with 'python'.")
        
        code = code.removeprefix("python").strip()

        return code