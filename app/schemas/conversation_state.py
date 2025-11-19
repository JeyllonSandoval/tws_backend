from pydantic import BaseModel
from datetime import datetime
from app.models.conversation_state import ConversationStep


class ConversationStateBase(BaseModel):
    contact_number: str
    current_step: ConversationStep = ConversationStep.WAITING_NAME
    user_name: str | None = None
    product_name: str | None = None
    product_review: str | None = None
    wants_contact_again: str | None = None
    preferred_contact_method: str | None = None


class ConversationStateCreate(ConversationStateBase):
    pass


class ConversationStateUpdate(BaseModel):
    current_step: ConversationStep | None = None
    user_name: str | None = None
    product_name: str | None = None
    product_review: str | None = None
    wants_contact_again: str | None = None
    preferred_contact_method: str | None = None


class ConversationStateResponse(ConversationStateBase):
    state_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
