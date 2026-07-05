from pydantic import BaseModel

class LocationCreate(BaseModel):
	name: str
	description: str | None = None

class LocationResponse(BaseModel):
	id: int
	user_id: int
	name: str
	description: str | None = None

	class Config:
		from_attributes = True