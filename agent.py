import re
from litellm import completion

def build_system_message(tools):
    tool_descriptions = "\n".join([f'{{"name": "{tool.name}", "arguments": {tool.arguments}, "description": "{tool.description}"}}' for tool in tools])
    return {
        "role": "system",
        "content": f"""
You are a helpful agent.

Tools available to you are:

{tool_descriptions}

After request is complete, do not prompt for further engagement. If you have completed the task, use the "Terminate" tool to end the process.

Always respond in the following way. Do not add reasoning or commentary except in the message field:

```tool
{{
    "name": "<tool name>",
    "message": "<message>",
    "arguments": ["<tool arguments>"]
}}
```
        """
    }

def parse_tool_response(response_message):
    if response_message.startswith("```tool"):
        try:
            tool_response = re.split(r'```(tool)?', response_message)[2].strip()
            return eval(tool_response)
        except Exception as e:
            print(f"Error parsing tool response: {e}")
            return None
    else:
        print(response_message)
        return None

class Memory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self):
        return self.messages

    def get_last_message(self):
        return self.messages[-1] if self.messages else None

class Agent:
    def __init__(self, config, tools):
        self.memory = Memory()
        self.config = config
        self.system_message = build_system_message(tools)

    def send_message(self):
        response = completion(
            model = self.config["model"],
            messages = [self.system_message] + self.memory.get_messages(),
            api_base = self.config["api_base"],
        )

        return response.choices[0].message.content

    def run(self):
        while True:
            try:
                message = ""

                if(not self.memory.get_last_message() or self.memory.get_last_message()["role"] == "assistant"):
                    message = input("What do you want to do? " if len(self.memory.get_messages()) == 0 else "=> ")

                    self.memory.add_message("user", message)

                response_message = self.send_message()

                self.memory.add_message("assistant", response_message)

                tool_response = parse_tool_response(response_message)

                print(tool_response)

                if tool_response and tool_response.get("name").lower() == "message":
                    tool_response["arguments"] = [message]
                    self.memory.add_message("user", f"continue")

                if tool_response and tool_response.get("name").lower() == "terminate":
                    print("Terminating the agent process.")
                    break
                
            except Exception as e:
                print(f"An error occurred: {e}")
                break

