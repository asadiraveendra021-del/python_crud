from fastapi import APIRouter, Depends, UploadFile, File   # <-- add File here
from sqlalchemy.orm import Session
from database import get_db
from logger import logger
from schemas.post import PostCreate, PostResponse
from services.post_service import PostService
from auth import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(get_current_user)]
)

# ------------------- Create Post -------------------
@router.post("/user/{user_id}", response_model=PostResponse)
def create_post_for_user(user_id: int, post: PostCreate = Depends(), file: UploadFile | None = File(None), db: Session = Depends(get_db)):
    logger.info(f"Attempting to create post for user_id={user_id}, title={post.title}")
    new_post = PostService.create_post(user_id, post, db, file)
    logger.info(f"Post created successfully: post_id={new_post.id}")
    return new_post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate = Depends(), file: UploadFile | None = File(None), db: Session = Depends(get_db)):
    logger.info(f"Attempting to update post_id={post_id}, new_title={post.title}")
    updated_post = PostService.update_post(post_id, post, db, file)
    logger.info(f"Post updated successfully: post_id={updated_post.id}")
    return updated_post

# ------------------- Get All Posts -------------------
@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = PostService.get_all_posts(db)
    logger.info(f"Fetched all posts, count={len(posts)}")
    return posts

# ------------------- Get Single Post -------------------
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching post_id={post_id}")
    post = PostService.get_post_by_id(post_id, db)
    logger.info(f"Post fetched successfully: post_id={post.id}")
    return post

# ------------------- Delete Post -------------------
@router.delete("/{post_id}", response_model=PostResponse)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Attempting to delete post_id={post_id}")
    deleted_post = PostService.delete_post(post_id, db)
    logger.info(f"Post deleted successfully: post_id={deleted_post.id}")
    return deleted_post
