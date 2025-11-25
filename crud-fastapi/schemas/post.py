# schemas/post.py
from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    image_filename: Optional[str] = None
    user_id: int

    class Config:
        orm_mode = True
