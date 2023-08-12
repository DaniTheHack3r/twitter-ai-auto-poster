from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.twitter import TwitterManager
from schemas.tweet import Tweet
from services.gpt import GPTManager
import os

load_dotenv()

consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

app = FastAPI()
app.title = 'Twitter AI auto posting'
app.version = '0.0.1'


@app.post('/generate-tweet', tags=['Tweet Management'])
def generate_tweet(tweet: Tweet):
    generated_tweet = GPTManager().generate_text(tweet.topic)
    
    tweet_response = TwitterManager(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    ).create_tweet(generated_tweet)

    return JSONResponse(status_code=201, content=jsonable_encoder(tweet_response))


app.post('/login', tags=['Auth'])
def login():
    return 'This is the login page'
