from sqlalchemy.ext.asyncio import AsyncSession
from schemas.document_schemas import DocumentCreate, DocUpdate, Status
from repository.document_repo import DocumentRepository
from models.document_model import Document
from fastapi import HTTPException, status
from uuid import UUID
from dependencies.loggers import logger
from models.task_model import Task
from repository.task_repo import TaskRepository
from dependencies.web_sockets import manager                              # ADD
from repository.dashboard_repo import DashboardRepository  # ADD


class DocumentServices:
    @staticmethod
    async def create_doc(task_id: UUID, file_path: str, current_user, db: AsyncSession):
        logger.info("Attempting file_path save")
        if not file_path:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No file found")
        task = await TaskRepository.get_task_by_id(task_id, db)
        if task.assigned_to != UUID(current_user["id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="task is not assigned to you")
        doc = Document(task_id=task_id, file_path=file_path, uploaded_by=UUID(current_user["id"]))
        return await DocumentRepository.create_doc(doc, db)

    @staticmethod
    async def approve_doc(document_id: UUID, db: AsyncSession):
        logger.info("Approving Document")
        doc = await DocumentRepository.get_by_id(document_id, db)
        if doc.status == "approved":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already approved")
        result = await DocumentRepository.aprove_doc(doc, db)

        stats = await DashboardRepository.get_stats(db)  
        await manager.broadcast(stats)                    

        return result

    @staticmethod
    async def reject_doc(reason: str, document_id: UUID, db: AsyncSession):
        logger.info("Rejecting Document")
        doc = await DocumentRepository.get_by_id(document_id, db)
        if doc.status == "rejected":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already Rejected")
        result = await DocumentRepository.reject_doc(reason, doc, db)

        stats = await DashboardRepository.get_stats(db)  
        await manager.broadcast(stats)                    

        return result

    @staticmethod
    async def update(data: DocUpdate, db: AsyncSession):
        logger.info("Update Status")
        document = await DocumentRepository.get_by_id(data.id, db)
        return await DocumentRepository.update_task(data, document, db)