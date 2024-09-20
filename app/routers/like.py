from fastapi import Response, status, HTTPException, APIRouter, Depends
from app.database import get_db
from app.schema import LikeBase
from typing import Tuple, Optional
from app import oauth2

router = APIRouter(prefix='/like', 
                   tags=['Like'])


#Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: LikeBase, db: Tuple = Depends(get_db), current_user: Tuple = Depends(oauth2.get_current_user)):
    conn, cur = db

    cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
    selected_post = cur.fetchone()
    
    if selected_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")

    cur.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s",(like.post_id, current_user[0]))
    
    found_like = cur.fetchone()
    
    if like.dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Post has already been liked")
        
        cur.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s)", (like.post_id, current_user[0]))
        conn.commit()
        return {"message": "vote added successfully"}
    
    elif like.dir == 0:
        if found_like:
            cur.execute("DELETE from likes WHERE post_id = %s AND user_id = %s",(like.post_id, current_user[0]))
            conn.commit()
            return {"message": "vote deleted successfully"}
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")


    

    



    #conn.commit()
    
    return {"message": "OKAY"}