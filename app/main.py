from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.reviews_router import router as reviews_router
from app.routes.twilio_webhook import router as twilio_webhook

app = FastAPI(
    title="TWS Backend API",
    description="Backend API for Twilio WhatsApp Sandbox",
    version="1.0.0"
)

# Configure CORS
# Get allowed origins from environment variable or use defaults
import os
from dotenv import load_dotenv
load_dotenv()

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,https://tws-project-jssr.vercel.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(reviews_router)
app.include_router(twilio_webhook)

@app.get("/")
def root():
    return {"message": "API TWS_BACKEND is running"}
