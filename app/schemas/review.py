# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    contact_number: str
    user_name: str
    product_name: str
    product_review: str
    preferred_contact_method: Optional[str] = None
    preferred_contact_again: Optional[bool] = False
class ReviewCreate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
