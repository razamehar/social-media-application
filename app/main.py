from fastapi import FastAPI
from app.routers import post, user, auth, like
from app.routers.models import create_tables
from app.database import get_db, close_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    conn, cur = get_db()
    try:
        create_tables(conn, cur)
    finally:
        close_db(conn, cur)  # Ensure resources are closed


# Include routers for the API endpoints
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)


@app.get("/")
def root():
    return {"message": "Hello world"}