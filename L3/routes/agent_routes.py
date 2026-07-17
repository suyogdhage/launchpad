from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.session import get_db
from dependencies.deps import get_current_user
from agentic.agent import run_agent

router = APIRouter(prefix="/buddy", tags=["Onboarding Buddy"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(body: ChatRequest,current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await run_agent(current_user["id"], body.message, db)
    except Exception as e:
        raise e