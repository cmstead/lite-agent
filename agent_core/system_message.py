import platform


def build_system_message(tools, prompt=None):
    tool_descriptions = "\n".join([f'{{"name": "{tool.name}", "arguments": {tool.arguments}, "description": "{tool.description}"}}' for tool in tools])
    return {
        "role": "system",
        "content": f"""
{prompt if prompt else "You are a helpful agent."}

You do not perform destructive actions like deleting files or hacking into remote systems. You can only provide information and guidance.

You are running on a {platform.system()} system with Python {platform.python_version()}.

After request is complete, do not prompt for further engagement. If you have completed the task, use the "Terminate" tool to end the process.

Always respond in the following way. Do not add reasoning or commentary except in the message field:

```tool
{{
    "name": "<tool name>",
    "message": "<message>",
    "arguments": ["<tool arguments>"]
}}
```

Tools available to you are:

{tool_descriptions}
        """
    }

