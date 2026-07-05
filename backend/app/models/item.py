from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base import Base

class Item(Base):
	__tablename__ = "items"

	id = Column(Integer, primary_key = True, index = True)
	box_id = Column(Integer, ForeignKey("containers.id"))
	name = Column(String, nullable = False)
	description = Column(String, nullable = True)