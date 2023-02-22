from fastapi import APIRouter, status, Depends, HTTPException
from .. import database, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/like',
    tags=['Likes']
)


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def like(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        print("not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    like_query = db.query(models.Like).filter(models.Like.post_id == id, models.Like.user_id == current_user.id)
    found_like = like_query.first()

        
    if found_like:
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "like deleted"}

    else:    
        new_like = models.Like(post_id = id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "like successful"}

