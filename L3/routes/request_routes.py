from uuid import UUID
from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.request_schema import RequestCreate
from dependencies.session import get_db
from dependencies.deps import get_current_user,access
from models.user_role import UserRole
from services.request_service import RequestService

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("/")
async def create_request(body: RequestCreate,current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await RequestService.create_request(UUID(current_user["id"]), body.description, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get("/my")
async def my_requests(current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await RequestService.get_my_requests(UUID(current_user["id"]), db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@router.get("/all")
async def all_requests(current_user=Depends(access([UserRole.MANAGER, UserRole.HR, UserRole.SUPERADMIN])),db: AsyncSession = Depends(get_db)):
    try:
        return await RequestService.get_all_requests(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@router.patch("/{request_id}/approve")
async def approve_request(request_id: UUID,user=Depends(access([UserRole.MANAGER, UserRole.HR, UserRole.SUPERADMIN])),current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await RequestService.approve_request(request_id,current_user,db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@router.patch("/{request_id}/reject")
async def reject_request(request_id: UUID,user=Depends(access([UserRole.MANAGER, UserRole.HR, UserRole.SUPERADMIN])),current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await RequestService.reject_request(request_id,current_user, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
