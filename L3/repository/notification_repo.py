from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.notification_model import Notification
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID


class NotificationRepository:
    @staticmethod
    async def create(notification: Notification, db: AsyncSession):
        try:
            db.add(notification)
            await db.commit()
            await db.refresh(notification)
            return notification
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_by_user(user_id: UUID, db: AsyncSession, limit: int = 50):
        try:
            result = await db.execute(
                select(Notification)
                .where(Notification.user_id == user_id)
                .order_by(Notification.created_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_unread_count(user_id: UUID, db: AsyncSession):
        try:
            result = await db.execute(
                select(func.count(Notification.id)).where(
                    Notification.user_id == user_id,
                    Notification.is_read == False,
                )
            )
            return result.scalar()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def mark_read(notification_id: UUID, user_id: UUID, db: AsyncSession):
        try:
            result = await db.execute(
                update(Notification)
                .where(Notification.id == notification_id, Notification.user_id == user_id)
                .values(is_read=True)
            )
            await db.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def mark_all_read(user_id: UUID, db: AsyncSession):
        try:
            await db.execute(
                update(Notification)
                .where(Notification.user_id == user_id)
                .values(is_read=True)
            )
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
