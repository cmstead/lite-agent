import os
import random
import readline
from litellm import completion
from agent_core import core_tools
from agent_core.tool_utils import parse_tool_response, print_tool_message
from agent_core.system_message import build_system_message

# Keep track of input history across prompts
readline.set_auto_history(True)

class Memory:
    def __init__(self):
        self.messages = []

    def clear(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-10:]
    
    def get_messages(self):
        return self.messages

    def get_last_message(self):
        return self.messages[-1] if self.messages else None
    
    def get_last_two_agent_messages(self):
        agent_messages = []
        message_length = len(self.messages)
        index = -1

        while message_length + index > 0 and len(agent_messages) < 2:
            if self.messages[index].get("role") == "assistant":
                agent_messages.append(self.messages[index].get("content"))
            index -= 1

        return agent_messages

class Agent:

    def __init__(self, config, tools, agent_prompt=None, initial_message=None):
        self.memory = Memory()
        self.loop_counter = 0
        self.config = config
        self.tools = tools + core_tools.tools
        self.system_message = build_system_message(self.tools, agent_prompt)
        self.waiting_options = ["cogitating", "thinking", "processing", "pondering", "analyzing", "evaluating", "considering", "reflecting", "deliberating"]
        if initial_message:
            self.memory.add_message("user", initial_message)

    def send_message(self):
        response = completion(
            model = self.config["model"],
            messages = [self.system_message] + self.memory.get_messages(),
            api_base = self.config["api_base"] if "api_base" in self.config else None,
            api_key = self.config["api_key"] if "api_key" in self.config else None,
        )

        return response.choices[0].message.content

    def handle_tool_response(self, tool_response, message):
        if type(tool_response) is str:
            print(f"Agent: {tool_response}")
            self.memory.add_message("user", "Cannot parse message. Please try again.")
            return

        if tool_response:
            tool = next((t for t in self.tools if t.name.lower() == tool_response.get("name").lower()), None)
            if tool:
                result = tool.execute(tool_response.get("arguments", []))
                if result is not None:
                    self.memory.add_message("user", f"Tool {tool.name} executed with result: {result}")
            else:
                print(f"Tool not found: {tool_response.get('name')}")
                self.memory.add_message("user", f"Tool not found: {tool_response.get('name')}")
        else:
            self.memory.add_message("user", f"No valid tool response received. Please try again.")

    def reset(self):
        self.memory.clear()
        self.loop_counter = 0

    def clear_screen(self):
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For macOS and Linux
            os.system('clear')

    def is_duplicate_call(self):
        agent_messages = self.memory.get_last_two_agent_messages()

        if len(agent_messages) > 1:
            try:
                message1 = parse_tool_response(agent_messages[0])
                message2 = parse_tool_response(agent_messages[1])

                return message1.get("name") == message2.get("name") and message1.get("message") == message2.get("message")
            except:
                print("Unparseable response detected. Exiting.")
                return True
        
        return False

    def run(self):
        while True:
            try:
                self.loop_counter += 1

                if self.loop_counter > 15:
                    print("Loop limit reached. Exiting.")
                    self.reset()

                message = ""

                if(not self.memory.get_last_message() or self.memory.get_last_message()["role"] == "assistant"):
                    message = input("What do you want to do? " if len(self.memory.get_messages()) == 0 else "=> ")

                    if message.lower() in ["/bye", "/quit", "/exit"]:
                        print('Goodbye!')
                        break

                    if message.lower() == "/clear":
                        self.reset()
                        self.clear_screen()
                        continue
                        
                    if message.lower().startswith("/instructions"):
                        self.memory.add_message("user", f"read and execute {message[len('/instructions '):]} instructions")
                    else:
                        self.memory.add_message("user", message)

                print(f"{self.waiting_options[random.randrange(len(self.waiting_options))]}...")
                response_message = self.send_message()

                self.memory.add_message("assistant", response_message)

                if self.is_duplicate_call():
                    self.reset()
                    continue

                tool_response = parse_tool_response(response_message)

                if type(tool_response) is str:
                    print(f"Agent: {tool_response}")
                    self.memory.add_message("user", "Cannot parse message. Please try again.")
                    continue

                print_tool_message(tool_response)

                if tool_response and tool_response.get("name").lower() == "terminate":
                    self.reset()
                    print("End of line.")
                    print("")

                self.handle_tool_response(tool_response, message)

            except Exception as e:
                print(f"An error occurred: {e}")
                print(f"Unable to continue current request. Please try again.")
                self.reset()
                print("")
                continue

