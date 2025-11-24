from sqlalchemy import Column, Integer, String, Text
from database import Base

class TaskMessages(Base):
    __tablename__ = "task_messages"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, unique=True, index=True)
    messages_blob = Column(Text)  # storing JSON as string
