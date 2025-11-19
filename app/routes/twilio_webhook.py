from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse

from app.database.database import SessionLocal
from app.schemas.review import ReviewCreate
from app.controllers.reviews_crud import create_review

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

    # Datos enviados por Twilio
    message = form.get("Body")
    phone = form.get("From")

    print(f"Mensaje recibido de {phone}: {message}")

    # Guardar en la base de datos
    review_data = ReviewCreate(
        contact_number=phone,
        user_name="WhatsApp User",
        product_name="N/A",
        product_review=message,
        preferred_contact_method="whatsapp",
        preferred_contact_again=False
    )

    created = create_review(db, review_data)

    # Responder a WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message("¡Gracias! Tu mensaje fue recibido y guardado correctamente.")

    return Response(content=str(twilio_resp), media_type="application/xml")
