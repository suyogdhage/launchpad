from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.session import get_db
from dependencies.deps import get_current_user
from services.notification_service import NotificationService


router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/my")
async def my_notifications(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return await NotificationService.get_my_notifications(UUID(current_user["id"]), db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/my/unread-count")
async def unread_count(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return {"count": await NotificationService.get_unread_count(UUID(current_user["id"]), db)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{notification_id}/read")
async def mark_read(notification_id: UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        ok = await NotificationService.mark_read(notification_id, UUID(current_user["id"]), db)
        if not ok:
            raise HTTPException(status_code=404, detail="Notification not found")
        return {"message": "Marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/read-all")
async def mark_all_read(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        await NotificationService.mark_all_read(UUID(current_user["id"]), db)
        return {"message": "All marked as read"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
