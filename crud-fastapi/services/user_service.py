from sqlalchemy.orm import Session
from models.user import User
from auth import hash_password, verify_password, create_jwt_token
from fastapi import HTTPException

class UserService:

    @staticmethod
    def register_user(user_data, db: Session):
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def login_user(user_data, db: Session):
        db_user = db.query(User).filter(User.username == user_data.username).first()
        if not db_user or not verify_password(user_data.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_jwt_token({"username": db_user.username})
        return {"access_token": token, "token_type": "bearer"}
