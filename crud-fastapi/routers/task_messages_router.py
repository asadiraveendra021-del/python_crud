from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from logger import logger
from schemas.task_messages import TaskMessagesCreate, TaskMessagesResponse
from services.task_messages_service import TaskMessagesService
from auth import get_current_user

router = APIRouter(
    prefix="/task-messages",
    tags=["Task Messages"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=TaskMessagesResponse)
def save_task_messages(task: TaskMessagesCreate, db: Session = Depends(get_db)):
    logger.info(f"Fetching and saving messages for task_id={task.task_id}")
    record = TaskMessagesService.fetch_messages(username="ravi", task_id=task.task_id, db=db)
    if not record:
        raise HTTPException(status_code=404, detail="No messages with replies to save")
    return record
