import re
from litellm import completion

system_message = {
    "role": "system",
    "content": """
You are a helpful agent.

Tools available to you are:

{
    "name": "ls",
    "arguments": [],
    "description": "Use this to list files in a directory.",
}
{
    "name": "cd",
    "arguments": ["directory"],
    "description": "Use this to change the current working directory.",
}
{
    "name": "cat",
    "arguments": [],
    "description": "Use this to concatenate and display file contents.",
}
{
    "name": "Terminate",
    "arguments": [],
    "description": "Use this to end the agent process."
}

Always respond in the following way. Do not add reasoning or commentary except in the message field:

```tool
{
    "name": "<tool name>",
    "message": "<message>",
    "arguments": ["<tool arguments>"]
}
```
                """
}

def parse_tool_response(response_message):
    if response_message.startswith("```tool"):
        try:
            tool_response = re.split(r'```(tool)?', response_message)[2].strip()
            print(tool_response)
            tool_response_dict = eval(tool_response)
            return tool_response_dict
        except Exception as e:
            print(f"Error parsing tool response: {e}")
            return None
    else:
        return None

messages = []

while True:
    try:
        message = input("What do you want to do? ")

        messages.append({
            "role": "user",
            "content": message
        })

        response = completion(
            model = "ollama/qwen2.5-coder:14b",
            messages = [system_message] + messages,
            api_base = "http://192.168.1.212:11434",
        )

        response_message = response.choices[0].message.content

        messages.append({
            "role": "assistant",
            "content": response_message
        })

        tool_response = parse_tool_response(response_message)

        print(f"Tool response: {tool_response}" if tool_response else "No tool response detected.")

        if tool_response and tool_response.get("name") == "Terminate":
            print("Terminating the agent process.")
            break
    except Exception as e:
        print(f"An error occurred: {e}")