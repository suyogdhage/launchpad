from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,Depends,Form,UploadFile,File,HTTPException,status
from fastapi.responses import Response
from starlette.concurrency import run_in_threadpool
from dependencies.session import get_db
from dependencies.s3 import UploadService
from services.document_service import DocumentServices
from repository.document_repo import DocumentRepository
from dependencies.deps import get_current_user,access
from models.user_role import UserRole
from uuid import UUID
from dependencies.loggers import logger
from schemas.document_schemas import DocUpdate


router=APIRouter(prefix="/document",tags=["Document"])

@router.get('/my')
async def my_documents(db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return await DocumentServices.get_my_documents(current_user, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get('/pending')
async def pending_documents(status: str = "pending", db:AsyncSession=Depends(get_db),current_user=Depends(access([UserRole.HR, UserRole.SUPERADMIN]))):
    try:
        return await DocumentServices.get_documents_by_status(status, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.post('/create')
async def create_doc(task_id:UUID=Form(...),file:UploadFile=File(...),db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        logger.info("Attempting file upload")
        if file:
            file_path, file_size = await UploadService.upload_file(file)
        return await DocumentServices.create_doc(task_id, file_path, file_size, current_user, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get('/download/{document_id}')
async def download_doc(document_id:UUID,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        doc = await DocumentRepository.get_by_id(document_id, db)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        user_id = str(current_user["id"])
        role = current_user.get("role")
        allowed_roles = {UserRole.HR.value, UserRole.SUPERADMIN.value, UserRole.MANAGER.value}
        if str(doc.uploaded_by) != user_id and role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        obj = await run_in_threadpool(UploadService.get_object, doc.file_path)
        content = await run_in_threadpool(obj["Body"].read)
        filename = doc.file_path.split("/")[-1]
        content_type = obj.get("ContentType") or "application/octet-stream"
        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
        return Response(content=content, media_type=content_type, headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch('/approve')
async def approve_doc(document_id:UUID,db:AsyncSession=Depends(get_db),current_user=Depends(access([UserRole.HR, UserRole.SUPERADMIN]))):
    try:
        logger.info("Approving Document")
        return await DocumentServices.approve_doc(document_id,db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.patch('/reject')
async def reject_doc(reason:str,document_id:UUID,db:AsyncSession=Depends(get_db),current_user=Depends(access([UserRole.HR, UserRole.SUPERADMIN]))):
    try:
        logger.info("Rejecting Document")
        return await DocumentServices.reject_doc(reason,document_id,db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
@router.patch('/update')
async def update(data:DocUpdate,current_user=Depends(access([UserRole.HR, UserRole.SUPERADMIN])),db:AsyncSession=Depends(get_db)):
    try:
        return await DocumentServices.update(data,db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
