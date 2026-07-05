from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base import Base

class Location(Base):
	__tablename__ = "locations"

	id = Column(Integer, primary_key = True, index = True)
	user_id = Column(Integer, ForeignKey("users.id"))
	name = Column(String, nullable = False)
	description = Column(String, nullable = True)