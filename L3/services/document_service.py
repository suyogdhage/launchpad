from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repo import UserRepository
from schemas.document_schemas import DocumentCreate, DocUpdate, Status
from repository.document_repo import DocumentRepository
from models.document_model import Document
from fastapi import HTTPException, status
from uuid import UUID
from dependencies.loggers import logger
from models.task_model import Task
from repository.task_repo import TaskRepository
from dependencies.web_sockets import manager                           
from repository.dashboard_repo import DashboardRepository  
from dependencies.email_service import email_service
from dependencies.s3 import UploadService
from services.notification_service import NotificationService
from config import settings

class DocumentServices:
    @staticmethod
    async def create_doc(task_id: UUID, file_path: str, file_size: int, current_user, db: AsyncSession):
        logger.info("Attempting file_path save")
        if not file_path:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No file found")
        task = await TaskRepository.get_task_by_id(task_id, db)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        if task.assigned_to != UUID(current_user["id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="task is not assigned to you")

        user_id = UUID(current_user["id"])
        quota_bytes = settings.USER_STORAGE_QUOTA_MB * 1024 * 1024
        total = await DocumentRepository.get_total_size_by_user(user_id, db)
        if (total or 0) + (file_size or 0) > quota_bytes:
            try:
                UploadService.delete_file(file_path)
            except Exception as e:
                logger.warning(f"Failed to clean up over-quota file: {e}")
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Storage quota of {settings.USER_STORAGE_QUOTA_MB} MB exceeded",
            )

        doc = Document(task_id=task_id, file_path=file_path, file_size=file_size, uploaded_by=user_id)
        return await DocumentRepository.create_doc(doc, db)

    @staticmethod
    async def get_my_documents(current_user, db: AsyncSession):
        user_id = UUID(current_user["id"])
        rows = await DocumentRepository.get_docs_by_user(user_id, db)
        return [
            {
                "id": doc.id,
                "task_id": doc.task_id,
                "file_path": doc.file_path,
                "file_size": doc.file_size,
                "status": doc.status,
                "rejection_reason": doc.rejection_reason,
                "created_at": doc.created_at,
                "task_title": title,
            }
            for doc, title in rows
        ]

    @staticmethod
    async def get_documents_by_status(status: str, db: AsyncSession):
        rows = await DocumentRepository.get_docs_by_status(status, db)
        return [
            {
                "id": doc.id,
                "task_id": doc.task_id,
                "file_path": doc.file_path,
                "file_size": doc.file_size,
                "status": doc.status,
                "rejection_reason": doc.rejection_reason,
                "created_at": doc.created_at,
                "task_title": title,
            }
            for doc, title in rows
        ]

    @staticmethod
    async def approve_doc(document_id: UUID, db: AsyncSession):
        logger.info("Approving Document")

        doc = await DocumentRepository.get_by_id(document_id, db)

        if doc.status == "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already approved",
            )

        result = await DocumentRepository.aprove_doc(doc, db)

    
        user = await UserRepository.get_user_by_id(doc.uploaded_by, db)

        if user:
            try:
                email_service.send_document_approved(user.email)
            except Exception as e:
                logger.warning(f"Approval email failed: {e}")
            await NotificationService.create_notification(
                user.id,
                "Document approved",
                f"Your document for task has been approved.",
                "/documents",
                db,
            )

        stats = await DashboardRepository.get_stats(db)
        await manager.broadcast(stats)

        return result

    @staticmethod
    async def reject_doc(reason: str, document_id: UUID, db: AsyncSession):
        logger.info("Rejecting Document")

        doc = await DocumentRepository.get_by_id(document_id, db)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        if doc.status == "rejected":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already rejected")

        result = await DocumentRepository.reject_doc(reason, doc, db)

        try:
            UploadService.delete_file(doc.file_path)
        except Exception as e:
            logger.warning(f"Failed to delete rejected file: {e}")

        user = await UserRepository.get_user_by_id(doc.uploaded_by, db)
        if user:
            try:
                email_service.send_document_rejected(user.email, reason)
            except Exception as e:
                logger.warning(f"Rejection email failed: {e}")
            await NotificationService.create_notification(
                user.id,
                "Document rejected",
                f"Your document was rejected: {reason}",
                "/documents",
                db,
            )

        return result

    @staticmethod
    async def update(data: DocUpdate, db: AsyncSession):
        logger.info("Update Status")
        document = await DocumentRepository.get_by_id(data.id, db)
        result = await DocumentRepository.update_task(data, document, db)
        if data.status == Status.rejected:
            try:
                UploadService.delete_file(document.file_path)
            except Exception as e:
                logger.warning(f"Failed to delete rejected file: {e}")
        return result
