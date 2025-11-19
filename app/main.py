# app/main.py
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, crud, schemas
from .database import SessionLocal, engine, Base
import os

app = FastAPI(title="TWS_BACKEND")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    # "https://frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "FastAPI backend listo"}

@app.get("/api/reviews", response_model=list[schemas.ReviewOut])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_reviews(db, skip=skip, limit=limit)
    return items

@app.post("/api/reviews", response_model=schemas.ReviewOut)
def create_review_endpoint(review_in: schemas.ReviewCreate, db: Session = Depends(get_db)):
    item = crud.create_review(db, review_in)
    return item

@app.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    from_number = form.get("From", "")
    body = form.get("Body", "")
    message_sid = form.get("MessageSid", None)

    if body:
        parts = [p.strip() for p in body.split("|")]
        if len(parts) >= 3:
            product, name, review_text = parts[0], parts[1], "|".join(parts[2:])
            review_in = schemas.ReviewCreate(
                contact_number=from_number,
                unique_id=message_sid,
                user_name=name,
                product_name=product,
                product_review=review_text
            )
            item = crud.create_review(db, review_in)
            twiml = f"<Response><Message>Gracias {name}, tu reseña para {product} fue registrada.</Message></Response>"
        else:
            twiml = "<Response><Message>Hola — por favor responde en el formato: producto|tu nombre|tu reseña</Message></Response>"
    else:
        twiml = "<Response><Message>No se recibió texto.</Message></Response>"

    return PlainTextResponse(twiml, media_type="application/xml")
