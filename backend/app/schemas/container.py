from pydantic import BaseModel

class BoxCreate(BaseModel):
	storage_area_id: int
	name: str
	description: str | None = None
	color: str | None = None

class BoxResponse(BaseModel):
	id: int
	storage_area_id: int
	name: str
	description: str | None = None
	color: str | None = None

	class Config:
		from_attributes = True