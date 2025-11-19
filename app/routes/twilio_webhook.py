from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse

from app.database.database import SessionLocal
from app.service.conversation_service import process_message, handle_restart_command

router = APIRouter(prefix="/twilio", tags=["Twilio"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/webhook")
async def twilio_webhook(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    # Data sent by Twilio
    message = form.get("Body") or ""
    phone = form.get("From") or ""

    print(f"Message received from {phone}: {message}")

    # Check for restart command (case insensitive)
    if message.strip().lower() == "restart":
        response_text = handle_restart_command(db, phone)
    else:
        # Process message through conversation flow
        response_text, is_completed = process_message(db, phone, message)

    # Respond to WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(response_text)

    return Response(content=str(twilio_resp), media_type="application/xml")
