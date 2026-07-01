import re
from litellm import completion

system_message = {
    "role": "system",
    "content": """
You are a helpful agent.

Tools available to you are:

{
    "name": "Terminal",
    "arguments": ["command to execute"],
    "description": "Use this to execute terminal commands.",
}
{
    "name": "Request",
    "arguments": ["message"],
    "description": "Use this for requests to the user."
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

class Memory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self):
        return self.messages

def parse_tool_response(response_message):
    if response_message.startswith("```tool"):
        try:
            tool_response = re.split(r'```(tool)?', response_message)[2].strip()
            return eval(tool_response)
        except Exception as e:
            print(f"Error parsing tool response: {e}")
            return None
    else:
        return None

class Agent:
    def __init__(self, config):
        self.memory = Memory()
        self.config = config

    def send_message(self):
        response = completion(
            model = self.config["model"],
            messages = [system_message] + self.memory.get_messages(),
            api_base = self.config["api_base"],
        )

        return response.choices[0].message.content

    def run(self):
        while True:
            try:
                message = input("What do you want to do? " if len(self.memory.get_messages()) == 0 else "=> ")

                self.memory.add_message("user", message)

                response_message = self.send_message()

                self.memory.add_message("assistant", response_message)

                tool_response = parse_tool_response(response_message)

                print(tool_response)

                if tool_response and tool_response.get("name").lower() == "terminate":
                    print("Terminating the agent process.")
                    break
                
            except Exception as e:
                print(f"An error occurred: {e}")
                break

