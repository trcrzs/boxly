from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base import Base

class Box(Base):
	__tablename__ = "containers"

	id = Column(Integer, primary_key = True, index = True)
	storage_area_id = Column(Integer, ForeignKey("storage_areas.id"))
	name = Column(String, nullable = False)
	description = Column(String, nullable = True)
	color = Column(String, nullable = True)