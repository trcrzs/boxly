from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
	email: str
	password: str

class UserCreate(BaseModel):
	name: str
	email: EmailStr
	password: str

class UserResponse(BaseModel):
	id: int
	name: str
	email: EmailStr
	role: str

	class Config:
		from_attributes = True