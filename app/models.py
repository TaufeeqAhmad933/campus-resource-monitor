from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(50))
    max_capacity = Column(Integer)
    location = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ResourceUsage(Base):
    __tablename__ = "resource_usage"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    current_load = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
