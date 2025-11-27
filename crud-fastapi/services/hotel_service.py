import requests
from sqlalchemy.orm import Session
from models.hotel_model import Hotel
from fastapi import HTTPException
from logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LITE_API_KEY")
API_URL = os.getenv("LITE_API_URL")


class HotelService:
    """
    Service layer responsible for syncing hotel details from LiteAPI
    and storing them into the database.
    """

    @staticmethod
    def sync_hotel(db: Session, hotel_id: str):
        """
        Sync hotel information from LiteAPI:
        - Fetch hotel details using external API
        - Create or update hotel record in local DB
        """
        logger.info("Starting hotel sync for hotel_id: %s", hotel_id)

        # Prepare API request
        headers = {"X-API-Key": API_KEY, "accept": "application/json"}

        try:
            response = requests.get(f"{API_URL}?hotelId={hotel_id}&timeout=4", headers=headers)
            response.raise_for_status()
            logger.info("LiteAPI response received successfully for hotel_id: %s", hotel_id)
        except Exception as e:
            logger.error("Failed to fetch hotel data from LiteAPI for hotel_id %s: %s", hotel_id, str(e))
            raise HTTPException(status_code=500, detail="Failed to fetch hotel data")

        data = response.json().get("data")

        if not data:
            logger.warning("No hotel data found in API for hotel_id: %s", hotel_id)
            raise HTTPException(status_code=404, detail="Hotel data not found from API")

        # Check if hotel exists or create new record
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            logger.info("Hotel record not found. Creating new hotel entry for hotel_id: %s", hotel_id)
            hotel = Hotel(id=hotel_id)

        # Update hotel fields
        hotel.name = data.get("name") or "No Name"
        hotel.description = data.get("hotelDescription")
        hotel.country = data.get("country")
        hotel.city = data.get("city")
        hotel.address = data.get("address")
        hotel.zip = data.get("zip")
        hotel.star_rating = data.get("starRating")
        hotel.latitude = data.get("location", {}).get("latitude")
        hotel.longitude = data.get("location", {}).get("longitude")

        # Save changes to database
        try:
            db.add(hotel)
            db.commit()
            db.refresh(hotel)
            logger.info("Hotel sync successful for hotel_id: %s", hotel_id)
        except Exception as e:
            logger.error("Database error while syncing hotel_id %s: %s", hotel_id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to sync hotel")

        return hotel
