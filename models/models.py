from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


#Basic pydantic model of user

class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None


#Model of how user will be in db. Inherits from User
class UserInDB(User):
    hashed_password: str


class Date_model(BaseModel):
    start_date: date
    end_date: date

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values, **kwargs):
        if 'start_date' in values and v <= values['start_date']:
            raise HTTPException(status_code=400, detail='End date must be after start date')
        return v