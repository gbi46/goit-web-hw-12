from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional

class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    user_id: int = None
    additional_info: Optional[str] = None

    class Config:
        from_attributes = True

class ContactResponse(BaseModel):
    id: int
    first_name: str = None
    last_name: str = None
    email: str = None
    phone: str = None
    birthday: date = None
    user_id: int = None
    additional_info: Optional[str] = None

    class Config:
        from_attributes = True

class ContactUpdate(ContactModel):
    done: bool

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"
