from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from repository.task_repo import TaskRepository
from services.request_service import RequestService
from services.task_service import TaskService
from schemas.task_schemas import TaskSchema

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

async def complete_task(user_id: UUID, task_title: str, db: AsyncSession):
    tasks = await TaskRepository.get_tasks_by_user(user_id, db)
    open_tasks = [t for t in tasks if t.status != "completed"]
    matches = [t for t in open_tasks if t.title.strip().lower() == task_title.strip().lower()]
    if not matches:
        matches = [t for t in open_tasks if task_title.strip().lower() in t.title.lower()]
    if not matches:
        return f"No pending task matching '{task_title}' found. Check your pending tasks first."
    task = matches[0]
    try:
        await TaskService.complete_task(task.id, {"id": str(user_id), "role": "new_hire"}, db)
    except HTTPException as e:
        return e.detail
    return f"Task '{task.title}' marked as completed!"

async def create_task(user_id: UUID, title: str, description: str | None, deadline: str | None, db: AsyncSession):
    parsed_deadline = None
    if deadline:
        try:
            parsed_deadline = date.fromisoformat(deadline)
        except ValueError:
            return f"Could not parse deadline '{deadline}'. Use YYYY-MM-DD format."
        if parsed_deadline <= date.today():
            return "Deadline must be a future date."
    schema = TaskSchema(title=title, description=description, assigned_to=user_id, deadline=parsed_deadline)
    try:
        task = await TaskService.create_task(schema, {"id": str(user_id), "role": "new_hire"}, db)
    except HTTPException as e:
        return e.detail
    return f"Task '{task.title}' created and assigned to you!"