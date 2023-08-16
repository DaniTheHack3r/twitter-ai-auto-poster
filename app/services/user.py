import os
from schemas.user import UserInDB


HASHED_PASSWORD = os.getenv('HASHED_PASSWORD')

fake_users_db = {
    "example": {
        "username": "example",
        "full_name": "example",
        "email": "example@example.com",
        "hashed_password": HASHED_PASSWORD,
    },
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)