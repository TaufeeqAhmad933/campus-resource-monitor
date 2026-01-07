from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app import models, schemas, crud
from app.load_engine import analyze_load, generate_recommendations

from fastapi.staticfiles import StaticFiles

# --------------------
# App initialization
# --------------------
app = FastAPI(title="Campus Resource Monitor")

# --------------------
# Database setup
# --------------------
models.Base.metadata.create_all(bind=engine)

# --------------------
# Serve Dashboard (VERY IMPORTANT)
# --------------------
app.mount(
    "/dashboard",
    StaticFiles(directory="dashboard", html=True),
    name="dashboard"
)

# --------------------
# Health check
# --------------------
@app.get("/")
def health_check():
    return {"status": "Backend running successfully"}

# --------------------
# APIs
# --------------------
@app.post("/resources")
def add_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return crud.create_resource(db, resource)

@app.post("/usage")
def report_usage(usage: schemas.UsageCreate, db: Session = Depends(get_db)):
    return crud.create_usage(db, usage)

@app.get("/analysis")
def analyze_resources(db: Session = Depends(get_db)):
    resources = crud.get_latest_resource_usage(db)

    analysis = analyze_load(resources)
    recommendations = generate_recommendations(
        analysis["overloaded"],
        analysis["underutilized"]
    )

    return {
        "analysis": analysis,
        "recommendations": recommendations
    }
