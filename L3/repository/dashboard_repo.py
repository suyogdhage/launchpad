from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import Users
from models.task_model import Task
from models.document_model import Document
from models.user_role import UserRole
from sqlalchemy.exc import SQLAlchemyError
from dependencies.web_sockets import WebSocket

class DashboardRepository:

    @staticmethod
    async def get_stats(db: AsyncSession):
        try:
            total_users = await db.scalar(select(func.count()).select_from(Users).where(Users.role_name == UserRole.NEW_HIRE))

            completed_tasks = await db.scalar( select(func.count()).select_from(Task).where(Task.status == "completed"))

            pending_tasks = await db.scalar(select(func.count()).select_from(Task) .where(Task.status == "pending") )

            pending_documents = await db.scalar(select(func.count()).select_from(Document).where(Document.status == "pending") )

            approved_documents = await db.scalar(select(func.count()).select_from(Document).where(Document.status == "approved") )

            rejected_documents = await db.scalar(select(func.count()).select_from(Document).where(Document.status == "rejected"))

            return {
                "total_new_hires": total_users,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "pending_document_reviews": pending_documents,
                "approved_documents": approved_documents,
                "rejected_documents": rejected_documents
            }
        except SQLAlchemyError as e:
            await db.rollback()
            raise e