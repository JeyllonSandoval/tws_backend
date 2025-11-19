from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from . import models
from .schemas import ReviewCreate

def create_review(db: Session, review: ReviewCreate):
    db_review = models.Review(
        contact_number=review.contact_number,
        unique_id=review.unique_id,
        user_name=review.user_name,
        product_name=review.product_name,
        product_review=review.product_review
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).order_by(models.Review.created_at.desc()).offset(skip).limit(limit).all()
