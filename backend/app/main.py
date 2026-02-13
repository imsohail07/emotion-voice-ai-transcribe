from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS (allow frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Emotion Voice AI Backend Started")

@app.get("/")
def root():
    return {"message": "Emotion Voice AI API is alive"}
