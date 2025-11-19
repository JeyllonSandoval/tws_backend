from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from datetime import datetime
import enum
from app.database.database import Base


class ConversationStep(str, enum.Enum):
    WAITING_NAME = "waiting_name"
    WAITING_PRODUCT_NAME = "waiting_product_name"
    WAITING_PRODUCT_REVIEW = "waiting_product_review"
    WAITING_CONTACT_AGAIN = "waiting_contact_again"
    WAITING_CONTACT_METHOD = "waiting_contact_method"
    COMPLETED = "completed"


class ConversationState(Base):
    __tablename__ = "conversation_states"

    state_id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    contact_number = Column(String(64), index=True, nullable=False, unique=True)
    current_step = Column(SQLEnum(ConversationStep), default=ConversationStep.WAITING_NAME, nullable=False)
    
    # Stored answers
    user_name = Column(String(128), nullable=True)
    product_name = Column(String(256), nullable=True)
    product_review = Column(Text, nullable=True)
    wants_contact_again = Column(String(10), nullable=True)  # "yes" or "no"
    preferred_contact_method = Column(String(128), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
