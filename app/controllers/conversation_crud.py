from sqlalchemy.orm import Session
from app.models.conversation_state import ConversationState, ConversationStep
from app.schemas.conversation_state import ConversationStateCreate, ConversationStateUpdate


def get_conversation_state(db: Session, contact_number: str):
    return db.query(ConversationState).filter(ConversationState.contact_number == contact_number).first()


def create_conversation_state(db: Session, data: ConversationStateCreate):
    new_state = ConversationState(
        contact_number=data.contact_number,
        current_step=data.current_step,
        user_name=data.user_name,
        product_name=data.product_name,
        product_review=data.product_review,
        wants_contact_again=data.wants_contact_again,
        preferred_contact_method=data.preferred_contact_method
    )
    db.add(new_state)
    db.commit()
    db.refresh(new_state)
    return new_state


def update_conversation_state(db: Session, contact_number: str, data: ConversationStateUpdate):
    state = get_conversation_state(db, contact_number)
    if state:
        if data.current_step is not None:
            state.current_step = data.current_step
        if data.user_name is not None:
            state.user_name = data.user_name
        if data.product_name is not None:
            state.product_name = data.product_name
        if data.product_review is not None:
            state.product_review = data.product_review
        if data.wants_contact_again is not None:
            state.wants_contact_again = data.wants_contact_again
        if data.preferred_contact_method is not None:
            state.preferred_contact_method = data.preferred_contact_method
        
        db.commit()
        db.refresh(state)
        return state
    return None


def reset_conversation_state(db: Session, contact_number: str):
    state = get_conversation_state(db, contact_number)
    if state:
        state.current_step = ConversationStep.WAITING_NAME
        state.user_name = None
        state.product_name = None
        state.product_review = None
        state.wants_contact_again = None
        state.preferred_contact_method = None
        db.commit()
        db.refresh(state)
        return state
    return None
