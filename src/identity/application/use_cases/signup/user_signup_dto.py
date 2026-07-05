from typing import Annotated
from pydantic import BaseModel, EmailStr, Field


class SignupInput(BaseModel):
    email: EmailStr
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    password: Annotated[str, Field(..., min_length=8, max_length=100)]

class SignupOutput(BaseModel):
    access_token: str
