import requests
import json
from sqlalchemy.orm import Session
from models.task_messages import TaskMessages
from fastapi import HTTPException
from logger import logger

class TaskMessagesService:

    LOGIN_URL = "https://iot.electems.com/task/api/api/auth/users"
    TARGET_URL = "https://iot.electems.com/task/api/messages"

    @staticmethod
    def fetch_messages(username: str, task_id: int, db: Session):
        try:
            #Get JWT token from login API
            login_payload = {"username": username}
            login_resp = requests.post(TaskMessagesService.LOGIN_URL, json=login_payload,verify=False)
            login_resp.raise_for_status()
            token = login_resp.json().get("token")
            if not token:
                raise HTTPException(status_code=401, detail="Failed to get JWT token")

            headers = {"Authorization": f"Bearer {token}"}

            # Call target messages API
            messages_resp = requests.get(f"{TaskMessagesService.TARGET_URL}?taskId={task_id}", headers=headers,verify=False)
            messages_resp.raise_for_status()
            messages_data = messages_resp.json()

            #  Filter response: only save messages with non-empty replies
            filtered_messages = [m for m in messages_data if m.get("replies")]

            if not filtered_messages:
                logger.info(f"No messages with replies found for task_id={task_id}")
                return None

            # Save to DB as JSON string
            messages_json_str = json.dumps(filtered_messages)

            # Check if task_id already exists
            existing = db.query(TaskMessages).filter(TaskMessages.task_id == task_id).first()
            if existing:
                existing.messages_blob = messages_json_str
                db.commit()
                db.refresh(existing)
                logger.info(f"Updated messages for task_id={task_id}")
                return existing

            new_record = TaskMessages(task_id=task_id, messages_blob=messages_json_str)
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            logger.info(f"Saved messages for task_id={task_id}")
            return new_record

        except requests.RequestException as e:
            logger.error(f"HTTP error while fetching messages: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch messages")
