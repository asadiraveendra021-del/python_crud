from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # 1-to-1 relationship back to User
    user = relationship("User", back_populates="profile")
