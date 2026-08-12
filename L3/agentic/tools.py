from uuid import UUID
from datetime import date
import re
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from repository.task_repo import TaskRepository
from repository.user_repo import UserRepository
from services.request_service import RequestService
from services.task_service import TaskService
from schemas.task_schemas import TaskSchema
from models.user_role import UserRole

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
        return f"[ERROR] No pending task matching '{task_title}' was found."
    task = matches[0]
    try:
        await TaskService.complete_task(task.id, {"id": str(user_id), "role": "new_hire"}, db)
    except HTTPException as e:
        return f"[ERROR] {e.detail}"
    return f"[SUCCESS] Task '{task.title}' was marked as completed."

async def _resolve_assignee(user_id: UUID, role: str, target: str | None, db: AsyncSession):
    if target and target.strip().lower() in {"me", "myself", "self", "mine", "i", "my"}:
        target = None
    if not target or not target.strip():
        return user_id, "yourself"
    raw = target.strip()
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", raw)
    email = email_match.group(0).lower() if email_match else None
    name_part = re.sub(r"\s*\(.*?\)\s*", " ", raw).strip() or raw
    users = await UserRepository.get_all_user(db)
    if email:
        for u in users:
            if u.email and u.email.strip().lower() == email:
                return u.id, u.name
        raise ValueError(f"Could not find anyone with email '{email}'.")
    needle = name_part.lower()
    for u in users:
        if u.email and u.email.strip().lower() == needle:
            return u.id, u.name
    for u in users:
        if u.name and u.name.strip().lower() == needle:
            return u.id, u.name
    matches = [u for u in users if u.name and needle in u.name.lower()]
    if len(matches) == 1:
        return matches[0].id, matches[0].name
    if len(matches) > 1:
        raise ValueError(f"Found multiple users matching '{name_part}'. Use the person's email instead.")
    raise ValueError(f"Could not find anyone named or emailed '{name_part}'.")

async def create_task(user_id: UUID, role: str, title: str, description: str | None, deadline: str | None, assigned_to: str | None, db: AsyncSession):
    parsed_deadline = None
    if deadline:
        try:
            parsed_deadline = date.fromisoformat(deadline)
        except ValueError:
            return f"[ERROR] Could not parse deadline '{deadline}'. Use YYYY-MM-DD format."
        if parsed_deadline <= date.today():
            return "[ERROR] Deadline must be a future date."
    try:
        assignee_id, assignee_label = await _resolve_assignee(user_id, role, assigned_to, db)
    except ValueError as e:
        return f"[ERROR] {e}"
    if assignee_id != user_id and role == UserRole.NEW_HIRE.value:
        return "[ERROR] You can only create tasks that are assigned to yourself."
    target = await UserRepository.get_user_by_id(assignee_id, db)
    if not target:
        return "[ERROR] Assigned user not found."
    if target.role_name == UserRole.SUPERADMIN:
        return "[ERROR] Cannot assign a task to a superadmin."
    schema = TaskSchema(title=title, description=description, assigned_to=assignee_id, deadline=parsed_deadline)
    try:
        task = await TaskService.create_task(schema, {"id": str(user_id), "role": role}, db)
    except HTTPException as e:
        return f"[ERROR] {e.detail}"
    return f"[SUCCESS] Task '{task.title}' was created and assigned to {assignee_label}. Task ID: {task.id}"