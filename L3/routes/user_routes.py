from services.user_services import UserServices
from fastapi import Depends,APIRouter,HTTPException,status
from dependencies.session import get_db
from schemas.user_schema import CreateUser,UserResponse,UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from dependencies.deps import get_current_user,access
from models.user_role import UserRole
from uuid import UUID
from repository.user_repo import UserRepository



router=APIRouter(prefix='/auth',tags=["Authentication"])

@router.post('/register',response_model=UserResponse)
async def register_user(user:CreateUser,db:AsyncSession=Depends(get_db),    current_user=Depends(access([UserRole.HR, UserRole.SUPERADMIN]))):
    try:
        return await UserServices.register_user(user,db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.post('/login')
async def login_user(user:UserLogin,db:AsyncSession=Depends(get_db)):
    return await UserServices.login_user(user,db)

@router.get('/user',response_model=List[UserResponse])
async def get_all_user(current_user=Depends(access([UserRole.HR, UserRole.SUPERADMIN, UserRole.MANAGER])),db:AsyncSession=Depends(get_db)):
    try:
        return await UserServices.get_all_user(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.patch('/assign')
async def assign_manager(user_id:UUID,manager_id:UUID,user=Depends(access([UserRole.HR, UserRole.SUPERADMIN])),current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await UserServices.assign_manager(user_id,manager_id,db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
@router.get('/me',response_model=UserResponse)
async def me(current_user=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    try:
        user=await UserRepository.get_user_by_id(UUID(current_user["id"]),db)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))