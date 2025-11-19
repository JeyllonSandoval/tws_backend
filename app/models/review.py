from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    contact_number = Column(String(64), index=True, nullable=False)
    unique_id = Column(String(128), index=True, nullable=True)
    user_name = Column(String(128), nullable=True)
    product_name = Column(String(256), nullable=False)
    product_review = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)