from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from typing import Tuple
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        # Attempt to decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Debugging: Print or log the payload to verify its structure
        print("Payload:", payload)  # This should print the decoded token payload
        
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schema.TokenData(user_id=int(user_id))

    except JWTError as e:
        # Print or log the error to see what went wrong during decoding
        print(f"JWT Error: {e}")
        raise credentials_exception

    return token_data

    
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Tuple = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # If token is received as JSON with access_token field
    if isinstance(token, str) and token.startswith('{'):
        import json
        token_data = json.loads(token)  # Parse the JSON token data
        token = token_data.get('access_token')  # Extract the actual access token
    
    print(f"Token received: {token}")  # Debugging: Print the extracted token
    
    token_data = verify_access_token(token, credentials_exception)
    
    # Fetch user by user_id from the database
    user_id = token_data.user_id
    conn, cur = db
    cur.execute("SELECT * FROM users WHERE id = %s LIMIT 1", (user_id,))
    user = cur.fetchone()

    return user
