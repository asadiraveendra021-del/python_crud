from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship


class EmailQueue(Base):
    __tablename__ = "email_queue"

    id = Column(Integer, primary_key=True, index=True)
    to_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    status = Column(String, default="PENDING")  # PENDING / SENT / FAILED
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

     # 🔥 One-to-One → EmailQueue belongs to exactly one Post
    post_id = Column(Integer, ForeignKey("posts.id"), unique=True)

    post = relationship("Post", back_populates="email_queue")
