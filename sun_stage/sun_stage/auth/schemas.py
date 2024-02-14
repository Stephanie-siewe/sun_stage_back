from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str 
    fullname: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password : str


class UserActivate(BaseModel):
    otp: str
    email: EmailStr

class InternCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str 
    fullname: str
    services: str
    period_start: datetime
    period_end: datetime
    
    
    

# Dependency to get the current user from the token

