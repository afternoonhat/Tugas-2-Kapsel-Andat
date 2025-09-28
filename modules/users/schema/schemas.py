from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from enum import Enum
import re

class Role(str, Enum):
    admin = "admin"
    staff = "staff"

class UserBase(BaseModel):
    username: str = Field(min_length=6, max_length=15, pattern=r'^[a-z0-9]+$') 
    email: EmailStr 
    role: Role

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)

    # Custom validator untuk password yang kompleks
    @field_validator('password')
    def validate_password(cls, v):
        # Harus mengandung alfanumerik dan hanya ! atau @ [cite: 8]
        if not re.match(r'^[a-zA-Z0-9!@]+$', v):
            raise ValueError('Password hanya boleh berisi karakter khusus hanya ! atau @')
        # Cek syarat minimal
        if not re.search(r'[A-Z]', v): # 1 huruf kapital [cite: 9]
            raise ValueError('Password harus mengandung minimal satu huruf kapital')
        if not re.search(r'[a-z]', v): # 1 huruf kecil [cite: 10]
            raise ValueError('Password harus mengandung minimal satu huruf kecil')
        if not re.search(r'[0-9]', v): # 1 angka [cite: 11]
            raise ValueError('Password harus mengandung minimal satu angka')
        if not re.search(r'[!@]', v): # 1 karakter khusus [cite: 12]
            raise ValueError('Password harus mengandung minimal satu karakter khusus ! atau @')
        return v

class UserInDB(UserBase):
    id: int
    hashed_password: str 
    created_at: datetime 
    updated_at: datetime 

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime