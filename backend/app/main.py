from fastapi import FastAPI

#api imports
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.locations import router as location_router
from app.api.storageareas import router as storage_areas_router
from app.api.containers import router as container_router
from app.api.items import router as item_router

#model imports
from app.models.user import User
from app.models.location import Location
from app.models.storagearea import StorageArea
from app.models.container import Box
from app.models.item import Item

#database imports
from app.database.base import Base
from app.database.session import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
	title = "Storage Management System API",
	description= "Backend API for organizing physical storage using containers, QR codes, and searchable inventory.",
	version= "0.1.0"
	)

#App routers
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(location_router)
app.include_router(storage_areas_router)
app.include_router(container_router)
app.include_router(item_router)

@app.get("/")
def root():
	return {"message": "Storage Management System API"}