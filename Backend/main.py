from fastapi import FastAPI
import uvicorn
from routes.authenticator import router as auth_router
from db.db import create_tables

app = FastAPI(title="Backend API", version="2.0.0")

# Create tables on startup
try:
    create_tables()
except Exception as e:
    print(f"Warning: Could not create tables on startup: {e}")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
