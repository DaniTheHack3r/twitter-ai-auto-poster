import os
from datetime import timedelta
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from typing import Annotated

from services.twitter import TwitterManager
from services.gpt import GPTManager
from services.user import fake_users_db
from schemas.tweet import Tweet
from schemas.token import Token
from utils.jwt import create_access_token, validate_token
from utils.password import authenticate_user

print('test')
print('test2')

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES=30

gpt_manager = {}
twitter_manager = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    gpt_manager["instance"] = GPTManager(OPENAI_API_KEY)
    twitter_manager["instance"] = TwitterManager(
        TWITTER_API_KEY,
        TWITTER_API_KEY_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET
    )
    yield
    gpt_manager.clear()
    twitter_manager.clear()


app = FastAPI(lifespan=lifespan)
app.title = 'Twitter AI auto posting'
app.version = '0.0.1'

@app.post("/login", response_model=Token, tags=["Auth"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return JSONResponse(content=jsonable_encoder(
        {"access_token": access_token, "token_type": "bearer"}
    ))

@app.post('/generate-tweet', 
    tags=['Tweet Management'],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(validate_token)]
)
async def generate_tweet(tweet: Tweet):
    generated_tweet = await gpt_manager["instance"].generate_text_with_chat_gpt(tweet.topic)
    tweet_response = await twitter_manager["instance"].create_tweet(generated_tweet)

    return JSONResponse(content=jsonable_encoder(tweet_response))
