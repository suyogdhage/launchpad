from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
import enum

class Status(str,enum.Enum):
    approved="approved"
    rejected="rejected"

class DocumentCreate(BaseModel):
    task_id:UUID

class DocUpdate(BaseModel):
    id:UUID
    status:Status
    reason :Optional[str]=Field(...,min_length=6,max_length=20)