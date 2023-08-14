from utils.http import HTTPManager
from fastapi.exceptions import HTTPException

class GPTManager():
    def __init__(self, openai_api_key) -> None:
        self.chat_completions_url = 'https://api.openai.com/v1/chat/completions'
        self.openai_api_key = openai_api_key

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

    async def generate_text_with_chat_gpt(self, prompt_request: str) -> str:
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {"role": "system", "content": self.prompt_system},
                {"role": "user", "content": self.prompt_user},
                {"role": "assistant", "content": self.prompt_assistant},
                {"role": "user", "content": prompt_request}
            ]
        }
        
        authorization_headers = {
            'Authorization': 'Bearer ' + self.openai_api_key
        }

        generated_response, status_code = await HTTPManager().post(
            self.chat_completions_url,
            payload,
            authorization_headers
        )

        if status_code != 200:
            raise HTTPException(
                status_code=status_code,
                detail="Request returned an error"
            )

        return generated_response['choices'][0]['message']['content'][1:-1]
