from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"

class createtask(TaskBase):
    pass

class taskupdate(BaseModel):
    title: Optional[str] = None
    desciption: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class taskresponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = (
            True
        )

