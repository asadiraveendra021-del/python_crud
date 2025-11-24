from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

    #one to one mapping because uselist=False if it is true means that column accepts list
    profile = relationship("UserProfile", back_populates="user", uselist=False)

    #one to many mapping because uselist=true , by default it will be true so did not mentioned explicitely
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
