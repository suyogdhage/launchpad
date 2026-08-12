from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.session import get_db
from dependencies.deps import get_current_user
from agentic.agent import run_agent
from repository.chat_repo import ChatRepository
from uuid import UUID

router = APIRouter(prefix="/buddy", tags=["Onboarding Buddy"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(body: ChatRequest,current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await run_agent(current_user["id"], current_user["role"], body.message, db)
    except Exception as e:
        raise e

@router.get("/history")
async def history(current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        messages = await ChatRepository.get_recent_messages(UUID(current_user["id"]), db)
        return [
            {"role": m.role.value, "content": m.content, "created_at": m.created_at}
            for m in messages
        ]
    except Exception as e:
        raise e