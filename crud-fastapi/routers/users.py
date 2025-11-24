from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse, UserLogin
from database import get_db
from logger import logger
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to register user: username={user.username}")
    new_user = UserService.register_user(user, db)
    logger.info(f"User registered successfully: user_id={new_user.id}")
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for username={user.username}")
    result = UserService.login_user(user, db)
    logger.info(f"Login successful for username={user.username}")
    return result
