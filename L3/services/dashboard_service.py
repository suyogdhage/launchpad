from repository.dashboard_repo import DashboardRepository
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.loggers import logger
from dependencies.web_sockets import manager


class DashboardService:
    @staticmethod
    async def get_stats(db: AsyncSession):

        logger.info("Getting Dashboard")
        stats = await DashboardRepository.get_stats(db)
        await manager.broadcast(stats)
        logger.info("Applied Websocket")
        return stats
    

 