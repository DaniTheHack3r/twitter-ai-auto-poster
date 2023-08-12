from requests_oauthlib import OAuth1Session
from fastapi.exceptions import HTTPException
import os
consumer_key = os.environ.get("API_KEY")

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
    
    def create_tweet(self, text) -> str:
        twitter = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

        response = twitter.post(
            'https://api.twitter.com/2/tweets',
            json={'text': text}
        )

        if response.status_code != 201:
            raise HTTPException(
                status_code=response.status_code,
                detail="Request returned an error: {} {}".format(response.status_code, response.text)
            )

        return response.json()
    
    def delete_tweet(self) -> None:
        return