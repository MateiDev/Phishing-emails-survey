import os
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import models, schemas, database

# Create tables 
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints  
@app.post("/api/user_info", response_model=schemas.UserInfo)
def submit_user_info(user: schemas.UserInfoCreate, db: Session = Depends(get_db)):
    db_user = models.UserInfo(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/api/email_assessment", response_model=schemas.EmailAssessment)
def submit_email_assessment(
    assessment: schemas.EmailAssessmentCreate, db: Session = Depends(get_db)
):
    db_assess = models.EmailAssessment(**assessment.model_dump())
    db.add(db_assess)
    db.commit()
    db.refresh(db_assess)
    return db_assess

# Static frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/{file_path:path}", include_in_schema=False)
async def serve_frontend(file_path: str):
    full_path = os.path.join(FRONTEND_DIR, file_path)
    if os.path.isfile(full_path):
        return FileResponse(full_path)
    # fallback 
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))