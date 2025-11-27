# services/post_service.py
import os
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from models.user import User
from models.post import Post
from models.email_queue import EmailQueue
from logger import logger

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class PostService:
    """
    Service layer for handling post-related operations:
    - Create post with optional image upload
    - Update post & image
    - Delete post & image file
    - Retrieve posts
    """

    @staticmethod
    def create_post(user_id: int, post_data, db: Session, file: UploadFile | None = None):
        """
        Create a new post:
        - Validates user
        - Saves image (optional)
        - Creates post record
        - Queues an email notification
        """
        logger.info("Attempting to create post for user_id: %s", user_id)

        # Validate user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning("Post creation failed: User %s not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")

        image_filename = None

        # Handle image upload
        if file:
            try:
                image_filename = f"{user_id}_{file.filename}"
                file_path = os.path.join(UPLOAD_FOLDER, image_filename)

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                logger.info("Image saved for user_id %s as %s", user_id, image_filename)
            except Exception as e:
                logger.error("Failed to save image for user_id %s: %s", user_id, str(e))
                raise HTTPException(status_code=500, detail="Failed to upload image")

        # Create post
        try:
            new_post = Post(
                **post_data.dict(),
                user_id=user_id,
                image_filename=image_filename
            )
            db.add(new_post)
            db.commit()
            db.refresh(new_post)
            logger.info("Post created successfully with post_id: %s", new_post.id)
        except Exception as e:
            logger.error("Database error while creating post for user_id %s: %s", user_id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create post")

        # Queue email notification
        try:
            email_subject = "Your post has been created"
            email_body = f"Hello {user.username},\n\nYour new post titled '{new_post.title}' was created successfully."

            email_job = EmailQueue(
                to_email=user.email,
                subject=email_subject,
                body=email_body,
                status="PENDING",
                post_id=new_post.id
            )
            db.add(email_job)
            db.commit()
            logger.info("Email queued for user_id %s regarding post_id %s", user_id, new_post.id)
        except Exception as e:
            logger.error("Failed to queue email for post_id %s: %s", new_post.id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to queue email")

        return new_post

    @staticmethod
    def update_post(post_id: int, post_data, db: Session, file: UploadFile | None = None):
        """
        Update an existing post:
        - Updates title and content
        - Handles image replacement (delete + upload)
        """
        logger.info("Updating post_id: %s", post_id)

        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logger.warning("Post update failed: post_id %s not found", post_id)
            raise HTTPException(status_code=404, detail="Post not found")

        # Update text content
        post.title = post_data.title
        post.content = post_data.content

        # Handle image update
        if file:
            try:
                # Delete old image
                if post.image_filename:
                    old_path = os.path.join(UPLOAD_FOLDER, post.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                        logger.info("Deleted old image for post_id %s", post_id)

                # Save new image
                new_filename = f"{post.user_id}_{file.filename}"
                file_path = os.path.join(UPLOAD_FOLDER, new_filename)

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                post.image_filename = new_filename
                logger.info("Updated image for post_id %s to %s", post_id, new_filename)

            except Exception as e:
                logger.error("Failed to update image for post_id %s: %s", post_id, str(e))
                raise HTTPException(status_code=500, detail="Failed to update image")

        # Save updated post
        try:
            db.commit()
            db.refresh(post)
            logger.info("Post updated successfully: post_id %s", post_id)
        except Exception as e:
            logger.error("Database error while updating post_id %s: %s", post_id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update post")

        return post

    @staticmethod
    def delete_post(post_id: int, db: Session):
        """
        Delete a post:
        - Deletes associated image (if exists)
        - Removes post record
        """
        logger.info("Deleting post_id: %s", post_id)

        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logger.warning("Delete failed: post_id %s not found", post_id)
            raise HTTPException(status_code=404, detail="Post not found")

        # Remove image file
        if post.image_filename:
            try:
                file_path = os.path.join(UPLOAD_FOLDER, post.image_filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info("Image deleted for post_id %s", post_id)
            except Exception as e:
                logger.error("Failed to delete image for post_id %s: %s", post_id, str(e))
                raise HTTPException(status_code=500, detail="Failed to delete post image")

        # Delete post
        try:
            db.delete(post)
            db.commit()
            logger.info("Post deleted successfully: post_id %s", post_id)
        except Exception as e:
            logger.error("Database error while deleting post_id %s: %s", post_id, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to delete post")

        return post

    @staticmethod
    def get_all_posts(db: Session):
        """
        Retrieve all posts.
        """
        logger.info("Fetching all posts")
        return db.query(Post).all()

    @staticmethod
    def get_post_by_id(post_id: int, db: Session):
        """
        Retrieve a single post by ID.
        """
        logger.info("Fetching post_id: %s", post_id)

        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logger.warning("Post not found: post_id %s", post_id)
            raise HTTPException(status_code=404, detail="Post not found")

        return post
