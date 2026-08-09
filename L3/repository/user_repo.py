from schemas.user_schema import CreateUser
from models.user_model import Users
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.auth import Authentication
from sqlalchemy import select, delete, update, func, or_
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from models.user_role import UserRole
from models.task_model import Task
from models.document_model import Document
from models.request_model import Request
from models.notification_model import Notification
from models.chat_model import Chat

class UserRepository:
    @staticmethod
    async def register_user(user:CreateUser,db:AsyncSession):
        try:
            user=Users(name=user.name,email=user.email,password=Authentication.hash_password(user.password),role_name=user.role_name)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_user_by_email(email:str,db:AsyncSession):
        try:
            result=await db.execute(select(Users).where(Users.email==email))
            return result.scalars().one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_all_user(db:AsyncSession):
        try:
            result=await db.execute(select(Users))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_user_by_id(id:UUID,db:AsyncSession):
        try:
            result=await db.execute(select(Users).where(Users.id==id))
            return result.scalars().one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def assign_manager(user:Users,manager_id:UUID,db:AsyncSession):
        try:
            user.assigned_to=manager_id
            await db.commit()
            return {f"{user.email} assigned to {manager_id}"}
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_team_members(manager_id: UUID, db: AsyncSession):
        try:
            result = await db.execute(select(Users).where(Users.assigned_to == manager_id))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def count_users_with_role(role: UserRole, db: AsyncSession):
        try:
            result = await db.execute(
                select(func.count()).select_from(Users).where(Users.role_name == role)
            )
            return result.scalar()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def delete_user_with_data(user_id: UUID, db: AsyncSession):
        try:
            await db.execute(
                update(Users).where(Users.assigned_to == user_id).values(assigned_to=None)
            )

            await db.execute(delete(Notification).where(Notification.user_id == user_id))
            await db.execute(delete(Chat).where(Chat.user_id == user_id))
            await db.execute(delete(Request).where(Request.request_by == user_id))

            task_result = await db.execute(
                select(Task.id).where(or_(Task.assigned_to == user_id, Task.assigned_by == user_id))
            )
            task_ids = list(task_result.scalars().all())

            doc_result = await db.execute(
                select(Document.file_path).where(
                    or_(
                        Document.uploaded_by == user_id,
                        Document.task_id.in_(task_ids) if task_ids else False,
                    )
                )
            )
            file_paths = list(doc_result.scalars().all())

            await db.execute(
                delete(Document).where(
                    or_(
                        Document.uploaded_by == user_id,
                        Document.task_id.in_(task_ids) if task_ids else False,
                    )
                )
            )
            if task_ids:
                await db.execute(delete(Task).where(Task.id.in_(task_ids)))

            await db.execute(delete(Users).where(Users.id == user_id))
            await db.commit()
            return file_paths
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

            
    


        

