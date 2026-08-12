from repository.task_repo import TaskRepository
from schemas.task_schemas import TaskSchema
from sqlalchemy.ext.asyncio import AsyncSession
from models.task_model import Task
from datetime import datetime, timezone
from fastapi import HTTPException, status
from dependencies.loggers import logger
from models.user_role import UserRole
from uuid import UUID
from repository.user_repo import UserRepository
from dependencies.web_sockets import manager                             
from repository.dashboard_repo import DashboardRepository  
from services.notification_service import NotificationService

class TaskService:
    @staticmethod
    async def create_task(data: TaskSchema, current_user, db: AsyncSession):
        logger.info("Creating Task")
        user = await UserRepository.get_user_by_id(data.assigned_to, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")
        if user.role_name == UserRole.SUPERADMIN:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot assign task to superadmin")
        if current_user["role"] == UserRole.MANAGER.value:
            if user.assigned_to is not None and UUID(current_user["id"]) != user.assigned_to:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User works under different manager")
        task = Task(title=data.title, description=data.description,
                    assigned_to=data.assigned_to,
                    assigned_by=UUID(current_user["id"]), deadline=data.deadline, status="pending")
        task = await TaskRepository.create_task(task, db)
        logger.info("Task Created Successfully")
        await NotificationService.create_notification(
            task.assigned_to,
            "New task assigned",
            f"Task '{task.title}' has been assigned to you.",
            "/tasks",
            db,
        )
        return task

    @staticmethod
    async def get_my_tasks(current_user, db: AsyncSession):
        logger.info("Getting Task")
        return await TaskRepository.get_tasks_by_user(current_user["id"], db)

    @staticmethod
    async def get_assigned_by_me(current_user, db: AsyncSession):
        logger.info("Getting tasks assigned by me")
        tasks = await TaskRepository.get_tasks_by_creator(current_user["id"], db)
        result = []
        for task in tasks:
            assignee = await UserRepository.get_user_by_id(task.assigned_to, db)
            result.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "deadline": task.deadline,
                "assigned_to": task.assigned_to,
                "assigned_by": task.assigned_by,
                "completed_at": task.completed_at,
                "created_at": task.created_at,
                "assignee_name": assignee.name if assignee else None,
                "documents": [
                    {
                        "id": d.id,
                        "task_id": d.task_id,
                        "file_path": d.file_path,
                        "file_size": d.file_size,
                        "status": d.status,
                        "rejection_reason": d.rejection_reason,
                        "created_at": d.created_at,
                    }
                    for d in task.documents
                ],
            })
        return result

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