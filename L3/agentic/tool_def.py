TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_pending_tasks",
            "description": "Get the pending tasks of the user, sorted by deadline. Use this when the user asks about their tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "submit_request",
            "description": "Submit a resource request on behalf of the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                },
                "required": ["description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark one of the user's onboarding tasks as completed. Use this when the user says they have finished, done, or completed a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_title": {
                        "type": "string",
                        "description": "Title of the task to mark as completed.",
                    }
                },
                "required": ["task_title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new onboarding task and assign it to the user. Use this when the user wants to add a task for themselves.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the new task."},
                    "description": {"type": "string", "description": "Optional details about the task."},
                    "deadline": {
                        "type": "string",
                        "description": "Optional deadline in YYYY-MM-DD format. Must be a future date.",
                    },
                },
                "required": ["title"],
            },
        },
    },
]