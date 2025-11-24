from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from logger import logger
from schemas.user_profile import UserProfileCreate, UserProfileResponse
from services.profile_service import ProfileService
from auth import get_current_user

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
    dependencies=[Depends(get_current_user)]
)

# ------------------- Create Profile -------------------
@router.post("/{user_id}", response_model=UserProfileResponse)
def create_profile(user_id: int, profile: UserProfileCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create profile for user_id={user_id}")
    new_profile = ProfileService.create_profile(user_id, profile, db)
    logger.info(f"Profile created successfully: profile_id={new_profile.id}")
    return new_profile

# ------------------- Get Profile -------------------
@router.get("/{user_id}", response_model=UserProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching profile for user_id={user_id}")
    profile = ProfileService.get_profile(user_id, db)
    logger.info(f"Profile retrieved successfully: profile_id={profile.id}")
    return profile

# ------------------- Update Profile -------------------
@router.put("/{user_id}", response_model=UserProfileResponse)
def update_profile(user_id: int, profile: UserProfileCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to update profile for user_id={user_id}")
    updated_profile = ProfileService.update_profile(user_id, profile, db)
    logger.info(f"Profile updated successfully: profile_id={updated_profile.id}")
    return updated_profile

# ------------------- Delete Profile -------------------
@router.delete("/{user_id}", response_model=UserProfileResponse)
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Attempting to delete profile for user_id={user_id}")
    deleted_profile = ProfileService.delete_profile(user_id, db)
    logger.info(f"Profile deleted successfully: profile_id={deleted_profile.id}")
    return deleted_profile
