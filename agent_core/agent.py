from litellm import completion
from agent_core import core_tools
from agent_core.tool_utils import parse_tool_response, print_tool_message
from agent_core.system_message import build_system_message

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
    def __init__(self, config, tools, agent_prompt=None):
        self.memory = Memory()
        self.config = config
        self.tools = tools + core_tools.tools
        self.system_message = build_system_message(self.tools, agent_prompt)

    def send_message(self):
        response = completion(
            model = self.config["model"],
            messages = [self.system_message] + self.memory.get_messages(),
            api_base = self.config["api_base"],
        )

        return response.choices[0].message.content

    def handle_tool_response(self, tool_response, message):
        if tool_response and tool_response.get("name").lower() == "message":
            tool_response["arguments"] = [message]
            self.memory.add_message("user", f"terminate session")
        elif tool_response:
            tool = next((t for t in self.tools if t.name.lower() == tool_response.get("name").lower()), None)
            if tool:
                result = tool.execute(tool_response.get("arguments", []))
                if result is not None:
                    self.memory.add_message("user", f"Tool {tool.name} executed with result: {result}")
                else:
                    self.memory.add_message("user", f"Tool {tool.name} executed successfully.")
            else:
                print(f"Tool not found: {tool_response.get('name')}")
                self.memory.add_message("user", f"Tool not found: {tool_response.get('name')}")
        else:
            self.memory.add_message("user", f"No valid tool response received. Please try again.")


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

                print_tool_message(tool_response)

                if tool_response and tool_response.get("name").lower() == "terminate":
                    print("Terminating the agent process.")
                    break

                self.handle_tool_response(tool_response, message)

            except Exception as e:
                print(f"An error occurred: {e}")
                break

