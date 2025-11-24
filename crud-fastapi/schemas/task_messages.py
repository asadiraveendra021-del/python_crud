from pydantic import BaseModel
from typing import List, Any

class TaskMessagesCreate(BaseModel):
    task_id: int

class TaskMessagesResponse(BaseModel):
    id: int
    task_id: int
    messages_blob: str

    class Config:
        orm_mode = True
