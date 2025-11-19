from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate


def get_reviews(db: Session):
    return db.query(Review).all()


def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.review_id == review_id).first()


def create_review(db: Session, data: ReviewCreate):
    new_review = Review(
        contact_number=data.contact_number,
        user_name=data.user_name,
        product_name=data.product_name,
        product_review=data.product_review,
        preferred_contact_method=data.preferred_contact_method,
        preferred_contact_again=data.preferred_contact_again
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def update_review(db: Session, review_id: int, data: ReviewCreate):
    review = get_review(db, review_id)
    if review:
        review.contact_number = data.contact_number
        review.user_name = data.user_name
        review.product_name = data.product_name
        review.product_review = data.product_review
        review.preferred_contact_method = data.preferred_contact_method
        review.preferred_contact_again = data.preferred_contact_again
        db.commit()
        db.refresh(review)
        return review
    return None

def delete_review(db: Session, review_id: int):
    review = get_review(db, review_id)
    if review:
        db.delete(review)
        db.commit()
        return True
    return False
