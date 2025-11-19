from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.review import ReviewCreate, ReviewResponse
from app.controllers.reviews_crud import (
    create_review,
    get_reviews,
    get_review,
    update_review,
    delete_review
)

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[ReviewResponse])
def list_reviews(db: Session = Depends(get_db)):
    return get_reviews(db)


@router.get("/{review_id}", response_model=ReviewResponse)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review no encontrada")
    return review


@router.post("/", response_model=ReviewResponse)
def create_new_review(data: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db, data)


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, data: ReviewCreate, db: Session = Depends(get_db)):
    updated = update_review(db, review_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Review no encontrada")
    return updated


@router.delete("/{review_id}")
def remove_review(review_id: int, db: Session = Depends(get_db)):
    deleted = delete_review(db, review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review no encontrada")
    return {"message": "Review eliminada con éxito"}
