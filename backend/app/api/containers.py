from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.container import Box
from app.schemas.container import BoxCreate, BoxResponse
from app.models.storagearea import StorageArea
from app.models.location import Location
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.item import Item

router = APIRouter(prefix="/containers", tags=["Boxes"])

@router.post("/", response_model = BoxResponse)
def create_box(box: BoxCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	storage_area = db.query(StorageArea).join(Location).filter(StorageArea.id == box.storage_area_id, Location.user_id == current_user.id).first()

	if storage_area is None:
		raise HTTPException(
			status_code = 404,
			detail = "Storage area does not exist."
			)

	new_box = Box(
		storage_area_id = box.storage_area_id,
		name = box.name,
		description = box.description,
		color = box.color
		)

	db.add(new_box)
	db.commit()
	db.refresh(new_box)

	return new_box

@router.get("/", response_model=list[BoxResponse])
def get_boxes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	return (db.query(Box).join(StorageArea).join(Location).filter(Location.user_id == current_user.id).all())

@router.get("/{box_id}", response_model=BoxResponse)
def get_box(box_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	box = (db.query(Box).join(StorageArea).join(Location).filter(Box.id == box_id, Location.user_id == current_user.id).first())

	if box is None:
		raise HTTPException(
			status_code=404,
			detail="Box not found."
			)

	return box

@router.put("/{box_id}", response_model=BoxResponse)
def update_box(box_id: int, updated_box: BoxCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	box = (db.query(Box).join(StorageArea).join(Location).filter(Box.id == box_id, Location.user_id == current_user.id).first())

	if box is None:
		raise HTTPException(
			status_code=404,
			detail="Box not found."
			)

	storage_area = db.query(StorageArea).join(Location).filter(StorageArea.id == updated_box.storage_area_id, Location.user_id == current_user.id).first()

	if storage_area is None:
		raise HTTPException(
			status_code = 404,
			detail = "Storage area not found."
			)

	box.storage_area_id = updated_box.storage_area_id
	box.name = updated_box.name
	box.description = updated_box.description
	box.color = updated_box.color

	db.commit()
	db.refresh(box)

	return box

@router.get("/{box_id}/qr")
def create_qr_code(box_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	box = (db.query(Box).join(StorageArea).join(Location).filter(Box.id == box_id, Location.user_id == current_user.id).first())

	if box is None:
		raise HTTPException(
			status_code = 404,
			detail = "Box not found."
			)

	box_url = f"http://127.0.0.1:8000/containers/public/{box_id}"
	qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={box_url}"

	return {
    "box_id": box_id,
    "box_url": box_url,
    "qr_code_url": qr_code_url
}

@router.get("/public/{box_id}")
def get_public_box(box_id: int, db: Session = Depends(get_db)):
	box = (db.query(Box).join(StorageArea).join(Location).filter(Box.id == box_id).first())

	if box is None:
		raise HTTPException(
			status_code = 404,
			detail = "Box not found."
			)
	items = db.query(Item).filter(Item.box_id == box_id).all()

	return {
		"box": box,
		"items": items
	}


@router.delete("/{box_id}")
def delete_box(box_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	box = (db.query(Box).join(StorageArea).join(Location).filter(Box.id == box_id, Location.user_id == current_user.id).first())

	if box is None:
		raise HTTPException(
			status_code = 404,
			detail="Box not found"
			)

	db.delete(box)
	db.commit()

	return{"message": "Box deleted successfully."}


