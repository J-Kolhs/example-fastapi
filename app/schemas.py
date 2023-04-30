from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Companies

class CompanyData(BaseModel):
    id: int
    companies_name: str

    class Config:
        orm_mode = True

class CompaniesCreate(BaseModel):
    companies_name: str

# User Authentication

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime
    companies: CompanyData
    is_verified: bool

    class Config:
        orm_mode = True

class UserAuthenticated(BaseModel):
    id: int

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    company_id: int
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResetPassword(BaseModel):
    password: str

class UserModify(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    created_at: Optional[datetime] = None
    roles: Optional[str] = None
    first_name: str
    last_name: str
    company_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class EmailSchema(BaseModel):
    email: EmailStr

# Bookings

class BookingBase(BaseModel):
    meeting_name: str
    meeting_start: datetime
    meeting_end: datetime

    class Config:
        orm_mode = True

class Booking(BookingBase):
    id: int
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class BookingCreate(BookingBase):
    pass

# Rooms

class RoomBase(BaseModel):
    id: int
    room_name: str

    class Config:
        orm_mode = True

class RoomOut(RoomBase):
    created_at: datetime

class RoomCreate(BaseModel):
    room_name: str

# Access

class AccessBase(BaseModel):
    user_id: int
    room_id: int

    class Config:
        orm_mode = True


class AccessOut(AccessBase):
    id: int
    created_at: datetime

class AccessView(AccessOut):
    user: UserOut
    


class UserData(UserOut):
    access: AccessBase


# Posts

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
    
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


# Votes 
class Vote(BaseModel):
    post_id: int
    dir: bool
