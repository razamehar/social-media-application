from fastapi import Response, status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
from schema import UserLogin, Token
from utils import verify
from oauth2 import oauth2
from typing import Tuple

router = APIRouter(prefix='/login', 
                   tags=['Authentication'])

# Login in.
@router.post("/", response_model=Token) # 
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Tuple = Depends(get_db)):
    conn, cur = db
    cur.execute("SELECT id, email, password FROM users where email = %s", (user_credentials.username,)) 
    user = cur.fetchone()
    
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")

    user_id, email, user_password = user
    

    if not verify(user_credentials.password, user_password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")
    
    access_token = oauth2.create_access_token(data={"user_id": user_id})
    
    return {"access_token": access_token, "token_type": "bearer"}