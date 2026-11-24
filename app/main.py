from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.calculations import router as calculations_router
from app.users import router as users_router, get_engine

app = FastAPI(title="IS601 Module 12: User and Calculation API", version="1.0.0")
app.include_router(users_router)
app.include_router(calculations_router)


@app.get("/")
def home():
    return {"message": "IS601 Module 12 API is running", "docs": "/docs"}


@app.get("/health")
def health():
    try:
        with Session(get_engine()) as session:
            session.execute(text("SELECT 1"))
        return {"app": "running", "database": "connected"}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
