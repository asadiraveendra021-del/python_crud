from sqlalchemy.orm import Session
from models.user import User
from models.user_profile import UserProfile
from fastapi import HTTPException
from logger import logger


class ProfileService:
    """
    Service layer responsible for managing user profile operations:
    - Create
    - Retrieve
    - Update
    - Delete
    """

    @staticmethod
    def create_profile(user_id: int, profile_data, db: Session):
        """
        Create a new profile for a user:
        - Validates if user exists
        - Ensures profile does not already exist
        - Saves profile in database
        """
        logger.info("Creating profile for user_id: %s", user_id)

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning("Profile creation failed: user_id %s not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")

        if user.profile:
            logger.warning("Profile creation failed: profile already exists for user_id %s", user_id)
            raise HTTPException(status_code=400, detail="Profile already exists")

        new_profile = UserProfile(**profile_data.dict(), user_id=user_id)

        try:
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            logger.info("Profile created successfully for user_id: %s", user_id)
        except Exception as e:
            logger.error("Database error while creating profile for user_id %s: %s", user_id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create profile")

        return new_profile

    @staticmethod
    def get_profile(user_id: int, db: Session):
        """
        Retrieve a user's profile by user_id.
        """
        logger.info("Fetching profile for user_id: %s", user_id)

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            logger.warning("Profile not found for user_id: %s", user_id)
            raise HTTPException(status_code=404, detail="Profile not found")

        logger.info("Profile fetched successfully for user_id: %s", user_id)
        return profile

    @staticmethod
    def update_profile(user_id: int, profile_data, db: Session):
        """
        Update existing user profile:
        - Validates profile existence
        - Updates only provided fields (partial update)
        """
        logger.info("Updating profile for user_id: %s", user_id)

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            logger.warning("Update failed: profile not found for user_id %s", user_id)
            raise HTTPException(status_code=404, detail="Profile not found")

        # Update only the fields provided in the request
        update_fields = profile_data.dict(exclude_unset=True)
        for key, value in update_fields.items():
            setattr(profile, key, value)

        try:
            db.commit()
            db.refresh(profile)
            logger.info("Profile updated successfully for user_id: %s", user_id)
        except Exception as e:
            logger.error("Database error while updating profile for user_id %s: %s", user_id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update profile")

        return profile

    @staticmethod
    def delete_profile(user_id: int, db: Session):
        """
        Delete a user profile from the database.
        """
        logger.info("Deleting profile for user_id: %s", user_id)

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            logger.warning("Delete failed: profile not found for user_id %s", user_id)
            raise HTTPException(status_code=404, detail="Profile not found")

        try:
            db.delete(profile)
            db.commit()
            logger.info("Profile deleted successfully for user_id: %s", user_id)
        except Exception as e:
            logger.error("Database error while deleting profile for user_id %s: %s", user_id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to delete profile")

        return profile
