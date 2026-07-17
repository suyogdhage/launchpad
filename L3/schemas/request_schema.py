from pydantic import BaseModel

class RequestCreate(BaseModel):
    description: str