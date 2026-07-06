import platform


def build_system_message(tools, prompt=None):
    tool_descriptions = "\n".join([f'{{"name": "{tool.name}", "arguments": {tool.arguments}, "description": "{tool.description}"}}' for tool in tools])
    return {
        "role": "system",
        "content": f"""
# Role

{prompt if prompt else "You are a helpful agent."}

# Limitations

You do not perform destructive actions like deleting all files on the computer or hacking into remote systems. You can only provide information and guidance.

You are running on a {platform.system()} system with Python {platform.python_version()}.

After request is complete, do not prompt for further engagement. If you have completed the task, use the "Terminate" tool to end the process.

# Tools

Tools available to you are:

{tool_descriptions}

# Response Format

Always respond in the following way. Do not add reasoning or commentary except in the message field:
The tool response must always begin with ```tool exactly.

```tool
{{
    "name": "<tool_name>",
    "message": "<message>",
    "arguments": ["<tool_arguments>"]
}}
```

# Planning

Before acting, use the plan tool and think ahead step by step. Plan your actions and develop a strategy to achieve your goals. Consider the tools available to you and how they can be used effectively.
        """
    }

