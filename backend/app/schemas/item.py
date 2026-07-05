from pydantic import BaseModel

class ItemCreate(BaseModel):
	box_id: int
	name: str
	description: str | None = None

class ItemResponse(BaseModel):
	id: int
	box_id: int
	name: str
	description: str | None = None

	class Config:
		from_attributes = True