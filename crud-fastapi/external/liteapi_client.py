import requests
import logging

logger = logging.getLogger(__name__)

class LiteAPIClient:
    BASE_URL = "https://api.liteapi.travel/v3.0/data"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "X-API-Key": self.api_key,
            "accept": "application/json"
        }

    def fetch_hotel_details(self, hotel_id: str) -> dict:
        """
        Calls LiteAPI V3 /data/hotel endpoint to fetch hotel details.
        """
        url = f"{self.BASE_URL}/hotel"
        params = {"hotelId": hotel_id, "timeout": 4}

        try:
            logger.info(f"Calling LiteAPI: {url} with hotelId={hotel_id}")
            response = requests.get(url, headers=self.headers, params=params, timeout=6)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"LiteAPI Response: {data}")
            return data
        except requests.exceptions.RequestException as ex:
            logger.error(f"LiteAPI request failed for hotel_id={hotel_id}: {ex}")
            raise
