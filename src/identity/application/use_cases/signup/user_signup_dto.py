from pydantic import BaseModel, EmailStr


class SignupInput(BaseModel):
    email: EmailStr
    name: str
    password: str

class SignupOutput(BaseModel):
    access_token: str
