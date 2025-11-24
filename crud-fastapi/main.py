from fastapi import FastAPI
from database import engine, Base
from routers import users, user_profile, post, task_messages_router
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from logger import logger

app = FastAPI()
Base.metadata.create_all(bind=engine)  # Create tables in DB

# need to include all our routers in main.py to enable the endpoints
app.include_router(users.router)
app.include_router(user_profile.router)
app.include_router(post.router)
app.include_router(task_messages_router.router)
# @app.get("/")
# def home():
#     logger.info("Root endpoint called")
#     return {"message": "FastAPI with PostgreSQL JWT Authentication is working!"}
