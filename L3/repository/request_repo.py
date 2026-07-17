from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.request_model import Request
from sqlalchemy.exc import SQLAlchemyError

class RequestRepository:

    @staticmethod
    async def create_request(request: Request, db: AsyncSession):
        try:
            db.add(request)
            await db.commit()
            await db.refresh(request)
            return request
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_request_by_id(request_id, db: AsyncSession):
        try:
            result = await db.execute(select(Request).where(Request.id == request_id))
            return result.scalars().one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_requests_by_user(user_id, db: AsyncSession):
        try:
            result = await db.execute(select(Request).where(Request.request_by == user_id))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_all_requests(db: AsyncSession):
        try:
            result = await db.execute(select(Request))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def save(db: AsyncSession):
        await db.commit()