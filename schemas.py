from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TodoCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
