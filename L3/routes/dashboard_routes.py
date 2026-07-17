from fastapi import APIRouter, Depends,WebSocket,HTTPException,status,WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.session import get_db
from dependencies.deps import role_checker
from services.dashboard_service import DashboardService
from repository.dashboard_repo import DashboardRepository
from dependencies.web_sockets import manager


router = APIRouter(prefix="/dashboard",tags=["Dashboard"])

@router.websocket("/ws")
async def dashboard_ws(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket)
    try:
        
        stats = await DashboardRepository.get_stats(db)
        await websocket.send_json(stats)

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/stats")
async def get_stats(current_user=Depends(role_checker("hr")),db: AsyncSession = Depends(get_db)):
    try:
        return await DashboardService.get_stats(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    


        