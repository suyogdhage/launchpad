from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from repository.task_repo import TaskRepository
from services.request_service import RequestService

async def get_pending_tasks(user_id: UUID, db: AsyncSession):
    tasks = await TaskRepository.get_tasks_by_user(user_id, db)
    pending = [t for t in tasks if t.status == "pending"]
    if not pending:
        return "You have no pending tasks!"
    sorted_tasks = sorted(pending, key=lambda t: (t.deadline is None, t.deadline))
    result = "Your pending tasks:\n"
    for t in sorted_tasks:
        deadline = str(t.deadline) if t.deadline else "No deadline"
        result += f"- {t.title} | Due: {deadline}\n"
    return result

async def submit_request(user_id: UUID, description: str, db: AsyncSession):
    request=await RequestService.create_request(user_id,description,db)
    return f"Request submitted! ID: {request.id}"