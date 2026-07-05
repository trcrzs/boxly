# create expiration times for login tokens
from datetime import datetime, timedelta, timezone
# provides functions to create and verify JWTs
from jose import jwt

SECRET_KEY = "change-this-secret-key" # move to environment variable later
ALGORITHM = "HS256" # hashing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # minutes before login token expires

#create signed jwt 
def create_access_token(data):
	to_encode = data.copy()

	expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

	to_encode.update({"exp": expire})

	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
