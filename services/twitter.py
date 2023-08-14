from fastapi.exceptions import HTTPException
from utils.http import HTTPManager
from utils.oauth import sign_oauth

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
    
    async def create_tweet(self, text) -> str:
        payload = {'text': text}
        authorization_headers = sign_oauth(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            url=self.manage_tweets_url,
            http_method='POST',
        )

        posted_tweet_info, status_code = await HTTPManager().post(
            url=self.manage_tweets_url,
            data=payload,
            additional_headers=authorization_headers
        )

        if status_code != 201:
            raise HTTPException(
                status_code=status_code,
                detail="Request returned an error"
            )

        return posted_tweet_info
    
    def delete_tweet(self) -> None:
        return