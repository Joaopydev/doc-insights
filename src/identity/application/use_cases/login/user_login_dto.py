from pydantic import BaseModel, EmailStr


class LoginInput(BaseModel):
    email: EmailStr
    password: str

class LoginOutput(BaseModel):
    access_token: str
