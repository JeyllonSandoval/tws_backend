from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    contact_number: str
    user_name: str
    product_name: str
    product_review: str
    preferred_contact_method: str | None = None
    preferred_contact_again: bool = False


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    review_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
