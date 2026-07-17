from sqlalchemy import select
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models.task_model import Task

class TaskRepository:
    @staticmethod
    async def create_task(task:Task,db:AsyncSession):
        try:
            db.add(task)
            await db.commit()
            await db.refresh(task)
            return task
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def get_task_by_id(task_id:UUID,db:AsyncSession):
        result=await db.execute(select (Task).where(Task.id==task_id))
        return result.scalars().one_or_none()
    
    @staticmethod
    async def get_tasks_by_user(user_id:str,db:AsyncSession):
        result=await db.execute(select(Task).where(Task.assigned_to==UUID(user_id)))
        return result.scalars().all()
    
    @staticmethod
    async def update_task(db):
        await db.commit()