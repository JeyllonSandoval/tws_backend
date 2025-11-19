from fastapi import FastAPI
from app.routes.reviews_router import router as reviews_router

app = FastAPI()

app.include_router(reviews_router)

@app.get("/")
def root():
    return {"message": "API TWS_BACKEND is running"}
