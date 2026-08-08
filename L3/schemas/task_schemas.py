from pydantic import BaseModel,FutureDate
from uuid import UUID
from datetime import date,datetime

    
class TaskSchema(BaseModel):
    title:str
    description:str |None=None
    assigned_to:UUID 
    deadline:FutureDate |None=None

class UpdateTaskStatus(BaseModel):
    status:str

class TaskResponse(BaseModel):
    id:UUID
    title:str
    description:str | None = None
    status:str
    deadline:date | None = None
    assigned_to:UUID
    assigned_by:UUID
    completed_at:datetime | None = None




