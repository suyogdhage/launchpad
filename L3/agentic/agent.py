import json
from uuid import UUID
from groq import AsyncGroq
from sqlalchemy.ext.asyncio import AsyncSession
from agentic.tools import get_pending_tasks, submit_request
from agentic.tool_def import TOOL_DEFINITIONS
from config import settings
from models.chat_model import MessageRole
from repository.chat_repo import ChatRepository
from dependencies.loggers import logger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are Onboarding Buddy — a helpful assistant for new hires.
You help them check pending tasks and submit requests.
When you take an action, confirm what you did in plain English.
Use the conversation history below for context."""

async def run_agent(user_id: UUID, user_message: str, db: AsyncSession):

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

    if not assistant_message.tool_calls:
        reply = assistant_message.content
        await ChatRepository.save_message(user_id, MessageRole.assistant, reply, db)
        return {"reply": reply}

    tool_call = assistant_message.tool_calls[0]
    tool_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if tool_name == "get_pending_tasks":
        tool_result = await get_pending_tasks(user_id, db)

    elif tool_name == "submit_request":
        tool_result = await submit_request(user_id, args["description"], db)

    else:
        tool_result = "Unknown tool."

    messages.append({
        "role": "assistant",
        "content": assistant_message.content or "",
        "tool_calls": [{
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_name,
                "arguments": tool_call.function.arguments
            }
        }]
    })
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": tool_result})

    final_response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages)

    reply = final_response.choices[0].message.content or ""
    await ChatRepository.save_message(user_id, MessageRole.assistant, reply, db)
    return {"reply": reply}
