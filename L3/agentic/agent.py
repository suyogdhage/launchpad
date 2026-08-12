import json
import re
from uuid import UUID
from groq import AsyncGroq
from sqlalchemy.ext.asyncio import AsyncSession
from agentic.tools import get_pending_tasks, submit_request, complete_task, create_task
from agentic.tool_def import TOOL_DEFINITIONS
from config import settings
from models.chat_model import MessageRole
from repository.chat_repo import ChatRepository
from dependencies.loggers import logger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are Onboarding Buddy — a helpful assistant.
You help users check pending tasks, complete tasks, create tasks, and submit requests.
To create, complete, or submit anything you MUST call the appropriate tool - never claim to have done it without calling the tool.
NEVER claim that a task was created, completed, or a request submitted unless the tool result begins with [SUCCESS].
If the tool result begins with [ERROR], tell the user plainly that the action failed and explain why.
Use the conversation history below for context."""

TEXTUAL_TOOL_CALL_RE = re.compile(r"<function=(\w+)>\s*(\{.*?\})\s*</function>", re.DOTALL)

async def run_agent(user_id: UUID, user_role: str, user_message: str, db: AsyncSession):

    history = await ChatRepository.get_recent_messages(user_id, db)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({
            "role": msg.role.value,
            "content": msg.content,
        })
    messages.append({"role": "user", "content": user_message})

    await ChatRepository.save_message(user_id, MessageRole.user, user_message, db)

    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=TOOL_DEFINITIONS)

    assistant_message = response.choices[0].message

    tool_name = None
    args = {}
    tool_call_id = None
    if assistant_message.tool_calls:
        tool_call = assistant_message.tool_calls[0]
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        tool_call_id = tool_call.id
    else:
        match = TEXTUAL_TOOL_CALL_RE.search(assistant_message.content or "")
        if match:
            try:
                tool_name = match.group(1)
                args = json.loads(match.group(2))
                tool_call_id = f"call_{tool_name}_{len(assistant_message.content)}"
            except (json.JSONDecodeError, ValueError):
                tool_name = None

    if not tool_name:
        reply = assistant_message.content
        await ChatRepository.save_message(user_id, MessageRole.assistant, reply, db)
        return {"reply": reply}

    if tool_name == "get_pending_tasks":
        tool_result = await get_pending_tasks(user_id, db)

    elif tool_name == "submit_request":
        tool_result = await submit_request(user_id, args["description"], db)

    elif tool_name == "complete_task":
        tool_result = await complete_task(user_id, args["task_title"], db)

    elif tool_name == "create_task":
        tool_result = await create_task(
            user_id, user_role, args["title"], args.get("description"),
            args.get("deadline"), args.get("assigned_to"), db,
        )

    else:
        tool_result = "Unknown tool."

    messages.append({
        "role": "assistant",
        "content": assistant_message.content or "",
        "tool_calls": [{
            "id": tool_call_id,
            "type": "function",
            "function": {
                "name": tool_name,
                "arguments": json.dumps(args)
            }
        }]
    })
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": tool_result})

    final_response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages)

    reply = final_response.choices[0].message.content or ""
    await ChatRepository.save_message(user_id, MessageRole.assistant, reply, db)
    return {"reply": reply}
