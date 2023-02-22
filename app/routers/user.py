from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas
from ..helpers import hash
from typing import List
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    users = db.query(models.User).all()

    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_schema: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash(user_schema.password)
    user_schema.password = hashed_password

    new_user = models.User(**user_schema.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user