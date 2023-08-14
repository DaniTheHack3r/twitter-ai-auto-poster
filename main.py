from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.twitter import TwitterManager
from schemas.tweet import Tweet
from services.gpt import GPTManager
from fastapi import status 
import os

load_dotenv()

consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
openai_api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()
app.title = 'Twitter AI auto posting'
app.version = '0.0.1'

gpt_manager = GPTManager(openai_api_key)
twitter_manager = TwitterManager(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

@app.post('/generate-tweet', tags=['Tweet Management'], status_code=status.HTTP_200_OK)
async def generate_tweet(tweet: Tweet):
    generated_tweet = await gpt_manager.generate_text_with_chat_gpt(tweet.topic)
    tweet_response = await twitter_manager.create_tweet(generated_tweet)

    return JSONResponse(content=jsonable_encoder(tweet_response))


@app.post('/login', tags=['Auth'])
def login():
    return 'This is the login page'
