from fastapi import Response, status, HTTPException, APIRouter, Depends
from app.database import get_db
from app.schema import PostBase
from typing import Tuple, Optional
from app import oauth2

router = APIRouter(prefix='/posts', 
                   tags=['Posts'])

# Retrieve all the posts
@router.get("/")
def get_posts(db: Tuple = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    conn, cur = db

    search = f"%{search}%"
    cur.execute("""
                SELECT posts.*, Count(likes.post_id) as votes
                FROM posts 
                LEFT JOIN likes ON posts.id = likes.post_id
                WHERE title LIKE %s 
                GROUP by posts.id
                LIMIT %s 
                OFFSET %s
                """, (search, limit, skip))
        
    posts = cur.fetchall()
    
    return (posts, current_user[1])

#Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostBase, db: Tuple = Depends(get_db), current_user: Tuple = Depends(oauth2.get_current_user)):
    conn, cur = db
    cur.execute(
        """
        INSERT INTO posts (title, content, published, user_id)
        VALUES (%s, %s, %s, %s) RETURNING *
        """,
        (post.title, post.content, post.published, current_user[0])
    )
    new_post = cur.fetchone()
    conn.commit()
    
    return new_post


# Retrieve a single post based on a specified id
@router.get("/{id}")
def get_post(id: int, db: Tuple = Depends(get_db), current_user: Tuple = Depends(oauth2.get_current_user)):
    conn, cur = db
    cur.execute("""
                SELECT posts.*, Count(likes.post_id) as votes
                FROM posts 
                LEFT JOIN likes ON posts.id = likes.post_id
                WHERE id = %s
                GROUP by posts.id
                """, (id,)) # Ensure id or any value is always passed as a tuple such as (id,)
    post = cur.fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    
    return (post, current_user[1])

# Delete a single post based on a specified id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Tuple = Depends(get_db), current_user: Tuple = Depends(oauth2.get_current_user)):
    conn, cur = db
    cur.execute("""
                SELECT * 
                FROM posts 
                WHERE id = %s
                """, (id,))
    selected_post = cur.fetchone()
    
    if selected_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")

    if selected_post[5] != current_user[0]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    cur.execute("""
                DELETE FROM posts 
                WHERE id = %s 
                RETURNING *
                """, (id,))
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update fields of an existing post
@router.put("/{id}")
def update_post(id: int, post: PostBase, db: Tuple = Depends(get_db), current_user: Tuple = Depends(oauth2.get_current_user)):
    conn, cur = db
    cur.execute("""
                SELECT * 
                FROM posts 
                WHERE id = %s
                """, (id,))
    selected_post = cur.fetchone()
    
    if selected_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")

    if selected_post[5] != current_user[0]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
                            (post.title, post.content, post.published, (id)))
    conn.commit()
    updated_post = cur.fetchone()
    
    return updated_post