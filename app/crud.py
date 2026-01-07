from sqlalchemy.orm import Session
from app import models, schemas

def create_resource(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(
        name=resource.name,
        type=resource.type,
        max_capacity=resource.max_capacity,
        location=resource.location
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def create_usage(db: Session, usage: schemas.UsageCreate):
    db_usage = models.ResourceUsage(
        resource_id=usage.resource_id,
        current_load=usage.current_load
    )
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage


from sqlalchemy import func

def get_latest_resource_usage(db: Session):
    results = (
        db.query(
            models.Resource.id,
            models.Resource.name,
            models.Resource.max_capacity,
            func.max(models.ResourceUsage.current_load).label("current_load")
        )
        .join(models.ResourceUsage, models.Resource.id == models.ResourceUsage.resource_id)
        .group_by(models.Resource.id)
        .all()
    )

    return [
        {
            "id": r.id,
            "name": r.name,
            "max_capacity": r.max_capacity,
            "current_load": r.current_load
        }
        for r in results
    ]
