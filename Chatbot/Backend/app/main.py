from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="A specialized legal Q&A system named Guardian.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
