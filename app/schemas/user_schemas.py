from pydantic import BaseModel, Field, EmailStr

#User Schema
class User(BaseModel):
    username : str = Field(min_length=3, max_length=20)
    email : EmailStr
    password : str = Field(min_length=8, max_length=100)

#User login schema
class UserLogin(BaseModel):
    identifier: str = Field(min_length=3, max_length=20)
    password : str = Field(min_length=8, max_length=100)



