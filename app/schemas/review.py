# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    contact_number: str
    unique_id: Optional[str] = None
    user_name: Optional[str] = None
    product_name: str
    product_review: str

class ReviewCreate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
