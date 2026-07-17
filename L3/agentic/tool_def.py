
TOOL_DEFINITIONS=[{
     "type": "function",
        "function": {
            "name": "get_pending_tasks",
            "description": "You need to get pending task of that particular user sorted by deadline.Use this when user asks about ",
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
            "description": "Submit resource request",
            "parameters": {
                "type": "object",
                "properties": {"description":{"type":"string"},
            },
            "required": ["description"],
        },
    }
    }
]