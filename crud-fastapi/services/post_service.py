# services/post_service.py
import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user import User
from models.post import Post
from models.email_queue import EmailQueue
from logger import logger

UPLOAD_FOLDER = "uploads"  # Folder to save images
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class PostService:

    @staticmethod
    def create_post(user_id: int, post_data, db: Session, file: UploadFile | None = None):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        image_filename = None
        if file:
            image_filename = f"{user_id}_{file.filename}"
            file_path = os.path.join(UPLOAD_FOLDER, image_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"Saved image file for post: {image_filename}")

        new_post = Post(**post_data.dict(), user_id=user_id, image_filename=image_filename)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        # Queue an email for sending
        email_subject = "Your post has been created"
        email_body = f"Hello {user.username},\n\nYour new post titled '{new_post.title}' was created successfully."
        email_job = EmailQueue(to_email=user.email, subject=email_subject, body=email_body, status="PENDING")
        db.add(email_job)
        db.commit()

        return new_post

    @staticmethod
    def update_post(post_id: int, post_data, db: Session, file: UploadFile | None = None):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        post.title = post_data.title
        post.content = post_data.content

        # Handle image update
        if file:
            if post.image_filename:
                # Remove old image
                old_path = os.path.join(UPLOAD_FOLDER, post.image_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            new_filename = f"{post.user_id}_{file.filename}"
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            post.image_filename = new_filename
            logger.info(f"Updated image for post: {new_filename}")

        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def delete_post(post_id: int, db: Session):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Remove image file if exists
        if post.image_filename:
            path = os.path.join(UPLOAD_FOLDER, post.image_filename)
            if os.path.exists(path):
                os.remove(path)
                logger.info(f"Deleted image file: {post.image_filename}")

        db.delete(post)
        db.commit()
        return post


    @staticmethod
    def get_all_posts(db: Session):
        return db.query(Post).all()

    @staticmethod
    def get_post_by_id(post_id: int, db: Session):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post


