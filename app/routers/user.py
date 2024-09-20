from fastapi import Response, status, HTTPException, APIRouter, Depends
from app.database import get_db
from app.schema import UserBase
from app.utils import hash
from typing import Tuple

router = APIRouter(prefix='/users', 
                   tags=['Users'])

# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED) # Any time a user is created, 201 should be sent
def create_users(user: UserBase, db: Tuple = Depends(get_db)):

    conn, cur = db
    hashed_pwd = hash(user.password)
    user.password = hashed_pwd
    try:
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *", 
                (user.email, user.password))
        new_user = cur.fetchone()
        conn.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"id": new_user[0],
            "email": new_user[1],
            "created_on": new_user[3]}


# Retrieve a single user info based on a specified id
@router.get("/{id}")
def get_users(id: int, db: Tuple = Depends(get_db)):
    conn, cur = db
    cur.execute("SELECT * FROM users where id = %s", (id,)) # Ensure id or any value is always passed as a tuple such as (id,)
    user = cur.fetchone()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found.")
    return {"id": user[0],
            "email": user[1],
            "created_on": user[3]}