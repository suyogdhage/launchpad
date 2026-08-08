from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
from datetime import datetime
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

class DocumentResponse(BaseModel):
    id: UUID
    task_id: UUID
    file_path: str
    file_size: int | None = None
    status: str
    rejection_reason: str | None = None
    created_at: datetime | None = None
    task_title: str | None = None