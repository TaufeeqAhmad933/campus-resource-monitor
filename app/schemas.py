from pydantic import BaseModel

class ResourceCreate(BaseModel):
    name: str
    type: str
    max_capacity: int
    location: str

class UsageCreate(BaseModel):
    resource_id: int
    current_load: int
