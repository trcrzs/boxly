from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.storagearea import StorageArea
from app.models.location import Location
from app.schemas.storagearea import StorageAreaCreate, StorageAreaResponse
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/storage_areas", tags=["Storage Areas"])

@router.post("/", response_model=StorageAreaResponse)
def create_storage_area(storage_area: StorageAreaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    location = db.query(Location).filter(
        Location.id == storage_area.location_id,
        Location.user_id == current_user.id
    ).first()

    if location is None:
        raise HTTPException(
        	status_code=404, 
        	detail="Location not found"
        	)

    new_storage_area = StorageArea(
        location_id=storage_area.location_id,
        name=storage_area.name,
        description=storage_area.description
    )

    db.add(new_storage_area)
    db.commit()
    db.refresh(new_storage_area)

    return new_storage_area

@router.get("/", response_model=list[StorageAreaResponse])
def get_storage_areas( db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (db.query(StorageArea).join(Location).filter(Location.user_id == current_user.id).all())

@router.get("/{storage_area_id}", response_model=StorageAreaResponse)
def get_storage_area(storage_area_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    storage_area = (db.query(StorageArea).join(Location).filter(StorageArea.id == storage_area_id, Location.user_id == current_user.id).first())

    if storage_area is None:
        raise HTTPException(
        	status_code=404, 
        	detail="Storage area not found"
        	)

    return storage_area

@router.put("/{storage_area_id}", response_model=StorageAreaResponse)
def update_storage_area(storage_area_id: int, updated_storage_area: StorageAreaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    storage_area = (db.query(StorageArea).join(Location).filter(StorageArea.id == storage_area_id, Location.user_id == current_user.id).first())

    if storage_area is None:
        raise HTTPException(status_code=404, detail="Storage area not found")

    location = db.query(Location).filter(Location.id == updated_storage_area.location_id, Location.user_id == current_user.id).first()

    if location is None:
        raise HTTPException(
        	status_code=404, 
        	detail="Location not found"
        	)

    storage_area.location_id = updated_storage_area.location_id
    storage_area.name = updated_storage_area.name
    storage_area.description = updated_storage_area.description

    db.commit()
    db.refresh(storage_area)

    return storage_area

@router.delete("/{storage_area_id}")
def delete_storage_area(storage_area_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    storage_area = (db.query(StorageArea).join(Location).filter(StorageArea.id == storage_area_id, Location.user_id == current_user.id).first())

    if storage_area is None:
        raise HTTPException(
        	status_code=404, 
        	detail="Storage area not found"
        	)

    db.delete(storage_area)
    db.commit()

    return {"message": "Storage area deleted successfully."}