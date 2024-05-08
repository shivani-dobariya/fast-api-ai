from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(UserLogin):
    full_name: str


class UserAll(UserCreate):
    id: int
