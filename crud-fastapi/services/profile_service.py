from sqlalchemy.orm import Session
from models.user import User
from models.user_profile import UserProfile
from fastapi import HTTPException

class ProfileService:

    @staticmethod
    def create_profile(user_id: int, profile_data, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.profile:
            raise HTTPException(status_code=400, detail="Profile already exists")

        new_profile = UserProfile(**profile_data.dict(), user_id=user_id)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile

    @staticmethod
    def get_profile(user_id: int, db: Session):
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    @staticmethod
    def update_profile(user_id: int, profile_data, db: Session):
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, key, value)

        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def delete_profile(user_id: int, db: Session):
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        db.delete(profile)
        db.commit()
        return profile
