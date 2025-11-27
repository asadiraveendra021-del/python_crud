from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.hotel_service import HotelService

router = APIRouter()
hotel_service = HotelService()

@router.get("/hotels/sync/{hotel_id}")
def sync_hotel(hotel_id: str, db: Session = Depends(get_db)):
    try:
        hotel = hotel_service.sync_hotel(db, hotel_id)
        return {"success": True, "hotel": {
            "id": hotel.id,
            "name": hotel.name,
            "description": hotel.description,
            "country": hotel.country,
            "city": hotel.city,
            "address": hotel.address,
            "zip": hotel.zip,
            "star_rating": hotel.star_rating,
            "latitude": hotel.latitude,
            "longitude": hotel.longitude
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
