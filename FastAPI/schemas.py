from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str 
    age: int
    gender: str
    phone_num: Optional[str] = None

class HealthcareProviderCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    specialty: str
    availability: str 
    location: str
    phone_num: Optional[str] = None  

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True 

class UserLogin(BaseModel):
    email: EmailStr
    password: str     

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None   

class SymptomsInput(BaseModel):
    symptoms: list[str]

class PrecautionsOut(BaseModel):
    precaution_1: str
    precaution_2: str
    precaution_3: str
    precaution_4: str   