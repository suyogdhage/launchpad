from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from models.request_model import Request
from repository.request_repo import RequestRepository
from repository.user_repo import UserRepository
from dependencies.loggers import logger

class RequestService:

    @staticmethod
    async def create_request(user_id: UUID, description: str, db: AsyncSession):
        logger.info("Creating Request")
        request = Request(request_by=user_id,description=description)
        return await RequestRepository.create_request(request, db)

    @staticmethod
    async def get_my_requests(user_id: UUID, db: AsyncSession):
        logger.info("Getting your request")
        return await RequestRepository.get_requests_by_user(user_id, db)

    @staticmethod
    async def get_all_requests(db: AsyncSession):
        logger.info("Getting all requests")
        return await RequestRepository.get_all_requests(db)

    @staticmethod
    async def approve_request(request_id: UUID,current_user,db: AsyncSession):
        logger.info("Approving Request")
        request = await RequestRepository.get_request_by_id(request_id, db)
        user=await UserRepository.get_user_by_id(request.request_by,db)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        if request.status != "pending":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Request is already {request.status}")
        if user.assigned_to!=current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized")
        request.status = "approved"
        await RequestRepository.save(db)
        return request

    @staticmethod
    async def reject_request(request_id: UUID,current_user, db: AsyncSession):
        logger.info("Rejecting Request")
        request = await RequestRepository.get_request_by_id(request_id, db)
        user=await UserRepository.get_user_by_id(request.request_by,db)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        if request.status != "pending":
            raise HTTPException(status_code=400, detail=f"Request is already {request.status}")
        if user.assigned_to!=current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized")
        request.status = "rejected"
        await RequestRepository.save(db)
        return request