from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,Depends,Form,UploadFile,File,HTTPException,status
from dependencies.session import get_db
from dependencies.s3 import UploadService
from services.document_service import DocumentServices
from dependencies.deps import get_current_user,role_checker
from uuid import UUID
from dependencies.loggers import logger
from schemas.document_schemas import DocUpdate


router=APIRouter(prefix="/document",tags=["Document"])

@router.post('/create')
async def create_doc(task_id:UUID=Form(...),file:UploadFile=File(...),db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        logger.info("Attempting file upload")
        if file:
            file_path=await UploadService.upload_file(file)
        return await DocumentServices.create_doc(task_id,file_path,current_user,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.patch('/approve')
async def approve_doc(document_id:UUID,db:AsyncSession=Depends(get_db),current_user=Depends(role_checker("hr"))):
    try:
        logger.info("Approving Document")
        return await DocumentServices.approve_doc(document_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
@router.patch('/reject')
async def reject_doc(reason:str,document_id:UUID,db:AsyncSession=Depends(get_db),current_user=Depends(role_checker("hr"))):
    try:
        logger.info("Rejecting Document")
        return await DocumentServices.reject_doc(reason,document_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
@router.patch('/update')
async def update(data:DocUpdate,current_user=Depends(role_checker("hr")),db:AsyncSession=Depends(get_db)):
    try:
        return await DocumentServices.update(data,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

    