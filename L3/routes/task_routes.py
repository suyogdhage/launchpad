from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from dependencies.session import get_db
from dependencies.deps import role_checker,get_current_user,access
from schemas.task_schemas import TaskSchema, TaskResponse
from services.task_service import TaskService

router = APIRouter(prefix="/tasks",tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
async def create_task(data:TaskSchema,current_user=Depends(access(["hr","manager"])),db: AsyncSession = Depends(get_db)):
    try:
        return await TaskService.create_task(data,current_user,db)
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get("/me", response_model=list[TaskResponse])
async def my_tasks(current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await TaskService.get_my_tasks(current_user,db)
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
@router.patch("/{task_id}/complete")
async def complete_task(task_id: UUID,current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        return await TaskService.complete_task(task_id,current_user,db)
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))