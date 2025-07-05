import os, collections
from pathlib import Path

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import database, models, schemas

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

BACKEND_DIR  = Path(__file__).resolve().parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend" 

templates = Jinja2Templates(directory=str(FRONTEND_DIR))

@app.get("/results", response_class=HTMLResponse, include_in_schema=False)
def results(request: Request, db: Session = Depends(get_db)):
    demo_age, demo_gender, demo_role = map(collections.Counter, ((), (), ()))

    reasons_by_email  = {i: collections.Counter() for i in range(1, 5)}
    remarks_by_email  = {i: []                    for i in range(1, 5)}
    scores_by_email   = {i: collections.Counter() for i in range(1, 5)}  # ★ NEW

    for u in db.query(models.UserInfo).all():
        demo_age[u.age_group]     += 1
        demo_gender[u.gender]     += 1
        demo_role[u.current_role] += 1

    for a in db.query(models.EmailAssessment).all():
        for r in a.reasons:
            reasons_by_email[a.email_number][r] += 1
        scores_by_email[a.email_number][a.authenticity_score] += 1      # ★ NEW
        if a.remarks:
            remarks_by_email[a.email_number].append(a.remarks)

    ctx = {
        "request": request,
        "demo_json": {"age": demo_age, "gender": demo_gender, "role": demo_role},
        "reasons_json":  reasons_by_email,
        "remarks_json":  remarks_by_email,
        "scores_json":   scores_by_email,      # ★ NEW
        "emails": list(reasons_by_email.keys()),
    }
    return templates.TemplateResponse("results.html", ctx)


# Static frontend

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