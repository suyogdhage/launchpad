from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.chat_model import Chat, MessageRole
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID


class ChatRepository:
    @staticmethod
    async def save_message(user_id: UUID, role: MessageRole, content: str, db: AsyncSession):
        try:
            message = Chat(user_id=user_id, role=role, content=content)
            db.add(message)
            await db.commit()
            return message
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_recent_messages(user_id: UUID, db: AsyncSession, limit: int = 20):
        try:
            result = await db.execute(
                select(Chat)
                .where(Chat.user_id == user_id)
                .order_by(Chat.created_at.desc())
                .limit(limit)
            )
            return list(reversed(result.scalars().all()))
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
