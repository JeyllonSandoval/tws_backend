from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from app.database.database import Base

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    contact_number = Column(String(64), index=True, nullable=False)
    user_name = Column(String(128), nullable=False)
    product_name = Column(String(256), nullable=False)
    product_review = Column(Text, nullable=False)
    preferred_contact_method = Column(String(128), nullable=True)
    preferred_contact_again = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
