from pydantic import BaseModel, Field


class Tweet(BaseModel):
    topic: str = Field(min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "A list of keywords separated by commas or a short sentence."
            }
        }