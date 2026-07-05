from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserLogin
from app.auth.password import verify_password
from app.auth.token import create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	existing_user = db.query(User).filter(User.email == form_data.username).first()

	if existing_user is None:
		raise HTTPException(
			status_code = 401, 
			detail = "Invalid email or password."
			)

	password_is_valid = verify_password(form_data.password, existing_user.password_hash)

	if not password_is_valid:
		raise HTTPException(
			status_code = 401,
			detail="Invalid email or password."
			)

	access_token = create_access_token({"sub": str(existing_user.id)})

	return {
		"access_token": access_token,
		"token_type": "bearer"
	}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
	return current_user