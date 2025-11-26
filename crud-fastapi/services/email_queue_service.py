from models.email_queue import EmailQueue
from sqlalchemy.orm import Session
from utils.email_sender import EmailSender
from logger import logger


class EmailQueueService:

    @staticmethod
    def process_pending_emails(db: Session):
        pending_emails = db.query(EmailQueue).filter(EmailQueue.status == "PENDING").all()

        if not pending_emails:
            logger.info("No pending emails found.")
            return

        logger.info(f"Found {len(pending_emails)} pending emails.")

        for email in pending_emails:
            try:
                sent = EmailSender.send_email(
                    to_email=email.to_email,
                    subject=email.subject,
                    body=email.body,
                    db=db,
                    post_id=email.post_id
                )

                if sent:
                    email.status = "SENT"
                    logger.info(f"Email sent successfully → email_id={email.id}")
                else:
                    email.status = "FAILED"
                    logger.warning(f"Email failed → email_id={email.id}")

            except Exception as e:
                email.status = "FAILED"
                logger.error(f"Exception while sending email → id={email.id}, error={e}")

            db.commit()
