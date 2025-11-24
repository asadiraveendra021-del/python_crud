from pydantic import BaseModel

class UserProfileBase(BaseModel):
    bio: str | None = None
    location: str | None = None
    phone: str | None = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int

    class Config:
        orm_mode = True
