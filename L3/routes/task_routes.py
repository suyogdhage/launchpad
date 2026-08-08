from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from dependencies.session import get_db
from dependencies.deps import get_current_user,access
from models.user_role import UserRole
from schemas.task_schemas import TaskSchema, TaskResponse
from services.task_service import TaskService

router = APIRouter(prefix="/tasks",tags=["Tasks"])

@router.get("/assigned-by-me")
async def assigned_by_me(current_user=Depends(access([UserRole.HR, UserRole.MANAGER, UserRole.SUPERADMIN])),db: AsyncSession = Depends(get_db)):
    try:
        return await TaskService.get_assigned_by_me(current_user, db)
    except HTTPException:
        raise
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.post("/", response_model=TaskResponse)
async def create_task(data:TaskSchema,current_user=Depends(access([UserRole.HR, UserRole.MANAGER, UserRole.SUPERADMIN])),db: AsyncSession = Depends(get_db)):
    try:
        return await TaskService.create_task(data,current_user,db)
    except HTTPException:
        raise
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get("/me", response_model=list[TaskResponse])
async def my_tasks(current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await TaskService.get_my_tasks(current_user,db)
    except HTTPException:
        raise
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
@router.patch("/{task_id}/complete")
async def complete_task(task_id: UUID,current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await TaskService.complete_task(task_id,current_user,db)
    except HTTPException:
        raise
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))