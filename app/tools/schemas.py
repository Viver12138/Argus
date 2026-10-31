TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "object",
                        "description": "The mathematical expression",
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_text",
            "description": "Process text according to the request operation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The input text"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "uppercase",
                            "lowercase",
                            "word_count"
                        ],
                        "description": "The text processing operation"
                    }
                },
                "required": ["text", "operation"],
                "additionalProperties": False
            }
        }
    }
]