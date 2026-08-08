from sqlalchemy.ext.asyncio import AsyncSession
from models.notification_model import Notification
from repository.notification_repo import NotificationRepository
from dependencies.loggers import logger
from uuid import UUID


class NotificationService:
    @staticmethod
    async def create_notification(user_id: UUID, title: str, message: str | None, link: str | None, db: AsyncSession):
        try:
            notification = Notification(user_id=user_id, title=title, message=message, link=link)
            return await NotificationRepository.create(notification, db)
        except Exception as e:
            logger.warning(f"Failed to create notification for {user_id}: {e}")
            return None

    @staticmethod
    async def get_my_notifications(user_id: UUID, db: AsyncSession):
        return await NotificationRepository.get_by_user(user_id, db)

    @staticmethod
    async def get_unread_count(user_id: UUID, db: AsyncSession):
        return await NotificationRepository.get_unread_count(user_id, db)

    @staticmethod
    async def mark_read(notification_id: UUID, user_id: UUID, db: AsyncSession):
        return await NotificationRepository.mark_read(notification_id, user_id, db)

    @staticmethod
    async def mark_all_read(user_id: UUID, db: AsyncSession):
        return await NotificationRepository.mark_all_read(user_id, db)
