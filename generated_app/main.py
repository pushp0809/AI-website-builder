"""FastAPI application for Employee Benefits Portal."""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from routes import router
from seed_data import seed_database

# Configuration from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed database if empty
seed_database(DATABASE_URL.replace("sqlite:///", ""))

# FastAPI app
app = FastAPI(
    title="Employee Benefits Portal",
    description="Information portal for employee benefits",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/benefits", response_class=HTMLResponse)
async def benefits_page(request: Request):
    """Benefits overview page."""
    return templates.TemplateResponse("benefits.html", {"request": request})


@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """FAQ page."""
    return templates.TemplateResponse("faq.html", {"request": request})


@app.get("/eligibility", response_class=HTMLResponse)
async def eligibility_page(request: Request):
    """Eligibility checker page."""
    return templates.TemplateResponse("eligibility.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact form page."""
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """Admin page to view messages."""
    return templates.TemplateResponse("admin.html", {"request": request})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors without exposing details."""
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
