from sqlalchemy import Column, String, Integer, Float, Text
from database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    country = Column(String)
    city = Column(String)
    address = Column(String)
    zip = Column(String)
    star_rating = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
