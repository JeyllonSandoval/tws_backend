from fastapi import FastAPI
from app.routes.reviews_router import router as reviews_router
from app.routes.twilio_webhook import router as twilio_webhook

app = FastAPI()

app.include_router(reviews_router)
app.include_router(twilio_webhook)

@app.get("/")
def root():
    return {"message": "API TWS_BACKEND is running"}
