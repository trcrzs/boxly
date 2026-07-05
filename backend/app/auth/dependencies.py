from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.token import SECRET_KEY, ALGORITHM
from app.database.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    current_user = db.query(User).filter(User.id == int(user_id)).first()

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return current_user