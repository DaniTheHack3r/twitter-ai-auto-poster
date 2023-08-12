import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

class GPTManager():
    def __init__(self) -> None:
        self.prompt_system = "You are a helpful assistant, distant, but loyal"
        self.prompt_assistant = """Just provide me with the topic keywords (10-15 words), 
        and I'll craft tweets within the 280-character limit based on those keywords."""
        self.prompt_user = """You are now my writer. You work for me writing
        down tweets of no more than 280 characters about a
        topic I would give you. Expect from me some words describing
        the topic. No more than 10-15 words though. Then you will 
        write a tweet down for me. Please include no more than one hashtag. You can use
        emojis when convenient and those tweets should be mainly advices. Only return
        the tweet, don't put words before or after."""

    def generate_text(self, prompt_request: str) -> str:
        generated_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": self.prompt_system},
                {"role": "user", "content": self.prompt_user},
                {"role": "assistant", "content": self.prompt_assistant},
                {"role": "user", "content": prompt_request}
            ]
        )

        return generated_response['choices'][0]['message']['content'][1:-1]
