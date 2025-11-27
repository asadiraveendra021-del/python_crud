from pydantic import BaseModel
from typing import Optional

class HotelCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    zip: Optional[str] = None
    star_rating: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True
