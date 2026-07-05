from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse
from app.models.storagearea import StorageArea
from app.models.container import Box
from app.models.location import Location
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model = ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	container = db.query(Box).join(StorageArea).join(Location).filter(Box.id == item.box_id, Location.user_id == current_user.id).first()

	if container is None:
		raise HTTPException(
			status_code = 404,
			detail = "Box does not exist."
			)
	new_item = Item(
		box_id = item.box_id,
		name = item.name,
		description = item.description
		)

	db.add(new_item)
	db.commit()
	db.refresh(new_item)

	return new_item

@router.get("/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	return (db.query(Item).join(Box).join(StorageArea).join(Location).filter(Location.user_id == current_user.id).all())

@router.get("/search", response_model = list[ItemResponse])
def search_item(name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	item = db.query(Item).join(Box).join(StorageArea).join(Location).filter(Item.name.ilike(f"%{name}%"), Location.user_id == current_user.id).all()

	if item is None:
		raise HTTPException(
			status_code = 404,
			detail = "Item not found."
			)

	return item

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	item = db.query(Item).join(Box).join(StorageArea).join(Location).filter(Item.id == item_id, Location.user_id == current_user.id).first()

	if item is None:
		raise HTTPException(
			status_code = 404,
			detail = "Item not found."
			)

	return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, updated_item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	item = db.query(Item).join(Box).join(StorageArea).join(Location).filter(Item.id == item_id, Location.user_id == current_user.id).first()

	if item is None:
		raise HTTPException(
			status_code = 404,
			detail = "Item not found."
			)

	box = db.query(Box).join(StorageArea).join(Location).filter(Box.id == updated_item.box_id, Location.user_id == current_user.id).first()

	if box is None:
		raise HTTPException(
			status_code = 404,
			detail = "Box not found."
			)

	item.box_id = updated_item.box_id
	item.name = updated_item.name
	item.description = updated_item.description

	db.commit()
	db.refresh(item)

	return item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	item = (db.query(Item).join(Box).join(StorageArea).join(Location).filter(Item.id == item_id, Location.user_id == current_user.id).first())

	if item is None:
		raise HTTPException(
			status_code = 404,
			detail = "Item not found."
			)

	db.delete(item)
	db.commit()

	return {"message": "Item deleted successfully."}