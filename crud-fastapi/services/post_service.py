from sqlalchemy.orm import Session
from models.user import User
from models.post import Post
from fastapi import HTTPException

class PostService:

    @staticmethod
    def create_post(user_id: int, post_data, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_post = Post(**post_data.dict(), user_id=user_id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def get_all_posts(db: Session):
        return db.query(Post).all()

    @staticmethod
    def get_post_by_id(post_id: int, db: Session):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    @staticmethod
    def update_post(post_id: int, post_data, db: Session):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        post.title = post_data.title
        post.content = post_data.content
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def delete_post(post_id: int, db: Session):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        db.delete(post)
        db.commit()
        return post
