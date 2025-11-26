# models/post.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    image_filename = Column(String, nullable=True)  # new column for image
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")

     # 🔥 One-to-One → A Post has exactly one EmailQueue record
    email_queue = relationship(
        "EmailQueue",
        back_populates="post",
        uselist=False,           # important: tells SQLAlchemy this is one-to-one
        cascade="all, delete-orphan"
    )