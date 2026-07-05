from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationResponse
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/", response_model = LocationResponse)
def create_location(location: LocationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	new_location = Location(
		user_id = current_user.id,
		name = location.name,
		description = location.description
		)

	db.add(new_location)
	db.commit()
	db.refresh(new_location)

	return new_location


@router.get("/", response_model=list[LocationResponse])
def get_locations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	return (
		db.query(Location).filter(Location.user_id == current_user.id).all()
		)

@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	location = db.query(Location).filter(Location.id == location_id, Location.user_id == current_user.id).first()

	if location is None:
		raise HTTPException(
			status_code = 404,
			detail = "Location not found"
			)

	return location

@router.put("/{location_id}", response_model=LocationResponse)
def update_location(location_id: int, location: LocationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	existing_location = db.query(Location).filter(Location.id == location_id, Location.user_id == current_user.id).first()
	if existing_location is None:
		raise HTTPException(
			status_code = 404,
			detail = "Location not found"
			)

	existing_location.name = location.name
	existing_location.description = location.description

	db.commit()
	db.refresh(existing_location)

	return existing_location

@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	location_to_delete = db.query(Location).filter(Location.id == location_id, Location.user_id == current_user.id).first()
	if location_to_delete is None:
		raise HTTPException(
			status_code = 404,
			deatil = "Location not found"
			)

	db.delete(location_to_delete)
	db.commit()
	return {"message": "Location deleted successfully."}