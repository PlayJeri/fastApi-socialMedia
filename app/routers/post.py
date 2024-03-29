from fastapi import Response ,status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas
from ..schemas import PostCreate
from typing import List, Optional
from ..oauth2 import get_current_user
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(
        models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)
        ).order_by(models.Post.created_at.desc()).limit(limit).offset(skip).all()

   
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post_schema: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    new_post = models.Post(user_id = current_user.id, **post_schema.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(
        models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    print(f"current user id: {current_user.id}")
    print(f"post id: {post.user_id}")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
 
    return post