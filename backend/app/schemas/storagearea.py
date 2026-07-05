from pydantic import BaseModel

class StorageAreaCreate(BaseModel):
	location_id: int
	name: str
	description: str | None = None

class StorageAreaResponse(BaseModel):
	id: int
	location_id: int
	name: str
	description: str | None = None

	class Config:
		from_attributes = True