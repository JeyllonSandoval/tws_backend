from sqlalchemy.orm import Session
import re
from app.models.conversation_state import ConversationStep
from app.schemas.conversation_state import ConversationStateCreate, ConversationStateUpdate
from app.controllers.conversation_crud import (
    get_conversation_state,
    create_conversation_state,
    update_conversation_state
)
from app.controllers.reviews_crud import create_review
from app.schemas.review import ReviewCreate


def _normalize_yes_no(message: str) -> str | None:
    """Normalize yes/no responses. Returns 'yes', 'no', or None if invalid."""
    normalized = message.strip().lower()
    
    # Accept variations of yes
    yes_variations = ['yes', 'y', 'ye', 'yep', 'yeah', 'sure', 'ok', 'okay', 'si', 'sí']
    # Accept variations of no
    no_variations = ['no', 'n', 'nope', 'nah', 'not']
    
    if normalized in yes_variations:
        return 'yes'
    elif normalized in no_variations:
        return 'no'
    else:
        return None


def _is_valid_name(name: str) -> tuple[bool, str]:
    """Validate name. Returns (is_valid, error_message)."""
    if not name or len(name.strip()) == 0:
        return False, "Please provide your name. It cannot be empty."
    
    name = name.strip()
    
    if len(name) < 3:
        return False, "Please provide a valid name (at least 3 characters)."
    
    if len(name) > 128:
        return False, "Name is too long. Please provide a shorter name (maximum 128 characters)."
    
    # Allow letters, spaces, hyphens, apostrophes, and common international characters
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-\'\.]+$', name):
        return False, "Please provide a valid name using only letters, spaces, hyphens, and apostrophes."
    
    return True, ""


def _is_valid_product_name(product_name: str) -> tuple[bool, str]:
    """Validate product name. Returns (is_valid, error_message)."""
    if not product_name or len(product_name.strip()) == 0:
        return False, "Please provide a product name. It cannot be empty."
    
    product_name = product_name.strip()
    
    if len(product_name) < 2:
        return False, "Please provide a valid product name (at least 2 characters)."
    
    if len(product_name) > 256:
        return False, "Product name is too long. Please provide a shorter name (maximum 256 characters)."
    
    return True, ""


def _is_valid_review(review: str) -> tuple[bool, str]:
    """Validate review. Returns (is_valid, error_message)."""
    if not review or len(review.strip()) == 0:
        return False, "Please provide your review. It cannot be empty."
    
    review = review.strip()
    
    if len(review) < 10:
        return False, "Please provide a more detailed review (at least 10 characters)."
    
    if len(review) > 5000:
        return False, "Review is too long. Please provide a shorter review (maximum 5000 characters)."
    
    return True, ""


def _is_valid_contact_method(method: str) -> tuple[bool, str]:
    """Validate contact method. Returns (is_valid, error_message)."""
    if not method or len(method.strip()) == 0:
        return False, "Please provide a contact method. It cannot be empty."
    
    method = method.strip()
    
    if len(method) < 2:
        return False, "Please provide a valid contact method (at least 2 characters)."
    
    if len(method) > 128:
        return False, "Contact method is too long. Please provide a shorter method name (maximum 128 characters)."
    
    # Accept common contact methods (flexible validation)
    normalized = method.lower()
    common_methods = ['whatsapp', 'email', 'phone', 'telephone', 'sms', 'text', 'call']
    
    # Check if it's a common method or contains valid characters
    if not any(common in normalized for common in common_methods):
        # Still allow custom methods but validate they're reasonable
        if not re.match(r'^[a-zA-Z0-9\s\-\+]+$', method):
            return False, "Please provide a valid contact method using only letters, numbers, spaces, hyphens, and plus signs."
    
    return True, ""


def process_message(db: Session, contact_number: str, message: str) -> tuple[str, bool]:
    """
    Process incoming message and return response text and completion status.
    
    Returns:
        tuple: (response_message, is_completed)
    """
    state = get_conversation_state(db, contact_number)
    
    # Normalize message
    message = message.strip()
    normalized_message = message.lower()
    
    # If no state exists, create one
    if not state:
        state_data = ConversationStateCreate(
            contact_number=contact_number,
            current_step=ConversationStep.WAITING_NAME
        )
        state = create_conversation_state(db, state_data)
        return "Hello! Thank you for contacting us. To get started, please provide your name.", False
    
    # Process based on current step
    if state.current_step == ConversationStep.WAITING_NAME:
        is_valid, error_msg = _is_valid_name(message)
        if not is_valid:
            return error_msg, False
        
        update_data = ConversationStateUpdate(
            user_name=message.strip(),
            current_step=ConversationStep.WAITING_PRODUCT_NAME
        )
        update_conversation_state(db, contact_number, update_data)
        return "Thank you! What is the name of the product you'd like to review?", False
    
    elif state.current_step == ConversationStep.WAITING_PRODUCT_NAME:
        is_valid, error_msg = _is_valid_product_name(message)
        if not is_valid:
            return error_msg, False
        
        update_data = ConversationStateUpdate(
            product_name=message.strip(),
            current_step=ConversationStep.WAITING_PRODUCT_REVIEW
        )
        update_conversation_state(db, contact_number, update_data)
        return "Great! Please share your review of this product.", False
    
    elif state.current_step == ConversationStep.WAITING_PRODUCT_REVIEW:
        is_valid, error_msg = _is_valid_review(message)
        if not is_valid:
            return error_msg, False
        
        update_data = ConversationStateUpdate(
            product_review=message.strip(),
            current_step=ConversationStep.WAITING_CONTACT_AGAIN
        )
        update_conversation_state(db, contact_number, update_data)
        return "Would you like us to contact you again? Please reply with 'yes' or 'no'.", False
    
    elif state.current_step == ConversationStep.WAITING_CONTACT_AGAIN:
        normalized_response = _normalize_yes_no(message)
        
        if normalized_response is None:
            return "I didn't understand your response. Please reply with 'yes' or 'no' to indicate if you'd like us to contact you again. (You can also use: yes, y, yeah, sure, ok, no, n, nope)", False
        
        wants_contact = normalized_response
        update_data = ConversationStateUpdate(
            wants_contact_again=wants_contact,
            current_step=ConversationStep.WAITING_CONTACT_METHOD if wants_contact == 'yes' else ConversationStep.COMPLETED
        )
        update_conversation_state(db, contact_number, update_data)
        
        if wants_contact == 'yes':
            return "What is your preferred contact method? (e.g., WhatsApp, Email, Phone)", False
        else:
            # Complete conversation and save review
            response_text, _ = _complete_conversation(db, state)
            return response_text, True
    
    elif state.current_step == ConversationStep.WAITING_CONTACT_METHOD:
        is_valid, error_msg = _is_valid_contact_method(message)
        if not is_valid:
            return error_msg, False
        
        update_data = ConversationStateUpdate(
            preferred_contact_method=message.strip(),
            current_step=ConversationStep.COMPLETED
        )
        update_conversation_state(db, contact_number, update_data)
        response_text, _ = _complete_conversation(db, state)
        return response_text, True
    
    elif state.current_step == ConversationStep.COMPLETED:
        return "Thank you! Your review has already been submitted. If you'd like to start a new review, please type 'restart'.", False
    
    return "I didn't understand that. Please try again.", False


def _complete_conversation(db: Session, state) -> tuple[str, bool]:
    """Complete the conversation and save the review. Returns (response_message, is_completed)."""
    # Get updated state
    updated_state = get_conversation_state(db, state.contact_number)
    
    if not updated_state:
        return "An error occurred while processing your review. Please try again by typing 'restart'.", False
    
    review_data = ReviewCreate(
        contact_number=updated_state.contact_number,
        user_name=updated_state.user_name or "Unknown",
        product_name=updated_state.product_name or "Unknown",
        product_review=updated_state.product_review or "",
        preferred_contact_method=updated_state.preferred_contact_method,
        preferred_contact_again=updated_state.wants_contact_again == 'yes'
    )
    
    try:
        create_review(db, review_data)
        return "Thank you for your review! Your feedback has been saved successfully. We appreciate your time.", True
    except Exception as e:
        print(f"Error saving review: {e}")
        return "An error occurred while saving your review. Please try again by typing 'restart'.", False


def handle_restart_command(db: Session, contact_number: str) -> str:
    """Handle restart command to begin a new conversation."""
    from app.controllers.conversation_crud import reset_conversation_state
    
    reset_conversation_state(db, contact_number)
    return "Great! Let's start over. Please provide your name."
