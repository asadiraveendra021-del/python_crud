from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from logger import logger
from services.email_queue_service import EmailQueueService


def process_pending_emails():
    """Job: Pick pending emails and send them."""
    logger.info("Scheduler started: Checking for pending emails...")

    db: Session = SessionLocal()

    try:
        EmailQueueService.process_pending_emails(db)
    except Exception as e:
        logger.error(f"Error while processing pending emails: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_pending_emails, "interval", minutes=1)
    scheduler.start()
    logger.info("APScheduler started successfully.")
