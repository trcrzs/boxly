from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base import Base

class StorageArea(Base):
	__tablename__ = "storage_areas"

	id = Column(Integer, primary_key = True, index = True)
	location_id = Column(Integer, ForeignKey("locations.id"))
	name = Column(String, nullable = False)
	description = Column(String, nullable = True)