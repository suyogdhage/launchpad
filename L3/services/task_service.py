from repository.task_repo import TaskRepository
from schemas.task_schemas import TaskSchema
from sqlalchemy.ext.asyncio import AsyncSession
from models.task_model import Task
from datetime import datetime, timezone
from fastapi import HTTPException, status
from dependencies.loggers import logger
from uuid import UUID
from repository.user_repo import UserRepository
from dependencies.web_sockets import manager                             
from repository.dashboard_repo import DashboardRepository  

class TaskService:
    @staticmethod
    async def create_task(data: TaskSchema, current_user, db: AsyncSession):
        logger.info("Creating Task")
        user = await UserRepository.get_user_by_id(data.assigned_to, db)
        if current_user["role"] == "manager" and UUID(current_user["id"]) != user.assigned_to:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User works under different manager")
        task = Task(title=data.title, description=data.description,
                    assigned_to=data.assigned_to,
                    assigned_by=current_user["id"], deadline=data.deadline, status="pending")
        task = await TaskRepository.create_task(task, db)
        logger.info("Task Created Successfully")
        return task

    @staticmethod
    async def get_my_tasks(current_user, db: AsyncSession):
        logger.info("Getting Task")
        return await TaskRepository.get_tasks_by_user(current_user["id"], db)

    @staticmethod
    async def complete_task(task_id: UUID, current_user, db: AsyncSession):
        logger.info("Attempting to complete")
        task = await TaskRepository.get_task_by_id(task_id, db)
        if not task:
            logger.warning("Task not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        if str(task.assigned_to) != current_user["id"]:
            logger.warning("Unauthorized Task completion attempt")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")
        if task.status == "completed":
            logger.warning("Task already completed")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task is already completed")
        task.status = "completed"
        task.completed_at = datetime.now(timezone.utc)
        await TaskRepository.update_task(db)
        logger.info(f"Task {task_id} completed successfully by user")

        stats = await DashboardRepository.get_stats(db)  
        await manager.broadcast(stats)                   

        return task