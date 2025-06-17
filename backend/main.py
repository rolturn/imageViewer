from fastapi import FastAPI
import os
from dotenv import load_dotenv
from api.images import router as images_router
from api.move_images import router as move_images_router
from api.auth import router as auth_router
from api.image import router as image_update_router
from api.export import router as export_router

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.getenv("BASE_DIR", "../images")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Include routers for endpoints
app.include_router(images_router, prefix="/api/images", tags=["Images"])
app.include_router(move_images_router, prefix="/api/move-images", tags=["Move Images"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(image_update_router, prefix="/api/image", tags=["Image Update"])
app.include_router(export_router, prefix="/api/export", tags=["Export"])
