from models.email_queue import EmailQueue
from sqlalchemy.orm import Session
from utils.email_sender import EmailSender
from logger import logger


class EmailQueueService:
    """
    Service for processing queued emails.
    Fetches pending emails, sends them, and updates their status.
    """

    @staticmethod
    def process_pending_emails(db: Session):
        """
        Process all emails with status 'PENDING':
        - Attempt to send each email via EmailSender
        - Update status to SENT or FAILED based on result
        - Log the full workflow
        """
        logger.info("Checking for pending emails to process...")

        # Fetch pending emails
        pending_emails = db.query(EmailQueue).filter(EmailQueue.status == "PENDING").all()

        if not pending_emails:
            logger.info("No pending emails found.")
            return

        logger.info("Found %s pending emails for processing.", len(pending_emails))

        # Process emails one-by-one
        for email in pending_emails:
            logger.info("Processing email_id=%s for recipient=%s", email.id, email.to_email)

            try:
                sent = EmailSender.send_email(
                    to_email=email.to_email,
                    subject=email.subject,
                    body=email.body,
                    db=db,
                    post_id=email.post_id
                )

                # Update email status
                if sent:
                    email.status = "SENT"
                    logger.info("Email sent successfully: email_id=%s", email.id)
                else:
                    email.status = "FAILED"
                    logger.warning("Email failed to send: email_id=%s", email.id)

            except Exception as e:
                # Log and mark as failed
                email.status = "FAILED"
                logger.error(
                    "Exception occurred while sending email (email_id=%s): %s",
                    email.id, str(e)
                )

            # Commit after each email to avoid batch failure
            try:
                db.commit()
            except Exception as commit_error:
                db.rollback()
                logger.error(
                    "Database commit failed after processing email_id=%s: %s",
                    email.id, str(commit_error)
                )
                # continue processing other emails gracefully

        logger.info("Email queue processing completed.")
