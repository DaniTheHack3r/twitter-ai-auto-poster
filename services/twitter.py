from fastapi.exceptions import HTTPException

from utils.http import post
from utils.oauth import sign_oauth1


class TwitterManager():
    def __init__(
        self, 
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.manage_tweets_url = 'https://api.twitter.com/2/tweets'

    def craft_payload(self, text: str) -> str:
        return {'text': text}
    
    def get_authorization_header(self):
        return sign_oauth1(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            url=self.manage_tweets_url,
            http_method='POST',
        )

    async def create_tweet(self, text: str) -> str:
        payload = self.craft_payload(text)
        authorization_header = self.get_authorization_header()

        posted_tweet_info, status_code = await post(
            url=self.manage_tweets_url,
            data=payload,
            additional_headers=authorization_header
        )

        if status_code != 201:
            raise HTTPException(
                status_code=status_code,
                detail="Request returned an error"
            )

        return posted_tweet_info
    
    def delete_tweet(self) -> None:
        return