from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "d403684989f4f63911c2695b996b93963e7bc76be9c8f482bab91d78db6dd74b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Ideally, you'd validate against a database
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
