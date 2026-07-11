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
    MAX_MESSAGES = 10

    def __init__(self):
        self.messages = []

    def clear(self):
        """Clear all messages in memory."""
        self.messages = []

    def add_message(self, role, content):
        """Add a new message to memory and maintain the message limit."""
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-self.MAX_MESSAGES:]
    
    def get_messages(self):
        """Retrieve all messages."""
        return self.messages

    def get_last_message(self):
        """Retrieve the last message if available."""
        return self.messages[-1] if self.messages else None
    
    def get_last_two_agent_messages(self):
        """Retrieve the last two messages from the assistant."""
        agent_messages = []
        for message in reversed(self.messages):
            if message.get("role") == "assistant":
                agent_messages.append(message.get("content"))
                if len(agent_messages) == 2:
                    break
        return agent_messages

class Agent:

    LOOP_LIMIT = 15

    def __init__(self, config, tools, agent_prompt=None, initial_message=None):
        self.memory = Memory()
        self.loop_counter = 0
        self.config = config
        self.tools = tools + core_tools.tools
        self.system_message = build_system_message(self.tools, agent_prompt)
        self.waiting_options = [
            "cogitating", "thinking", "processing", "pondering", 
            "analyzing", "evaluating", "considering", "reflecting", "deliberating"
        ]
        if initial_message:
            self.memory.add_message("user", initial_message)

    def send_message(self):
        """Send a message using the configured model and retrieve the response."""
        response = completion(
            model=self.config["model"],
            messages=[self.system_message] + self.memory.get_messages(),
            api_base=self.config.get("api_base"),
            api_key=self.config.get("api_key"),
        )
        return response.choices[0].message.content

    def handle_tool_response(self, tool_response, message):
        """Process the tool response and execute relevant actions."""
        if isinstance(tool_response, str):
            self._handle_invalid_response()
            return

        tool_name = tool_response.get("name")
        tool = next((t for t in self.tools if t.name.lower() == tool_name.lower()), None)

        if tool:
            result = tool.execute(tool_response.get("arguments", []))
            self.memory.add_message("user", f"Tool {tool.name} executed with result: {result}")
        else:
            print(f"Tool not found: {tool_name}")
            self.memory.add_message("user", f"Tool not found: {tool_name}")

    def reset(self):
        """Reset memory and loop counter."""
        self.memory.clear()
        self.loop_counter = 0

    def clear_screen(self):
        """Clear the screen based on the operating system."""
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)

    def is_duplicate_call(self):
        """Check if the last two responses are identical, indicating a duplicate call."""
        last_messages = self.memory.get_last_two_agent_messages()
        if len(last_messages) < 2:
            return False

        try:
            message1 = parse_tool_response(last_messages[0])
            message2 = parse_tool_response(last_messages[1])
            return message1.get("name") == message2.get("name") and message1.get("message") == message2.get("message")
        except:
            print("Unparseable response detected. Exiting.")
            return True

    def run(self):
        """Execute the main loop, handling user interaction and tool responses."""
        while True:
            try:
                self.loop_counter += 1

                if self.loop_counter > self.LOOP_LIMIT:
                    print("Loop limit reached. Exiting.")
                    self.reset()
                    break

                user_message = self._get_user_input()
                
                if user_message in ["/bye", "/quit", "/exit"]:
                    print('Goodbye!')
                    break

                if user_message == "/clear":
                    self.reset()
                    self.clear_screen()
                    continue

                self.memory.add_message("user", user_message)
                
                # Display a random waiting message
                print(f"{random.choice(self.waiting_options)}...")

                response_message = self.send_message()
                self.memory.add_message("assistant", response_message)

                if self.is_duplicate_call():
                    self.reset()
                    continue

                tool_response = parse_tool_response(response_message)
                print_tool_message(tool_response)

                if tool_response and tool_response.get("name").lower() == "terminate":
                    self.reset()
                    print("End of line.")
                    continue

                self.handle_tool_response(tool_response, user_message)

            except Exception as e:
                print(f"An error occurred: {e}")
                print(f"Unable to continue current request. Please try again.")
                self.reset()
                continue

    def _handle_invalid_response(self):
        """Handle cases where the tool response is invalid."""
        print("Agent: Cannot parse message. Please try again.")
        self.memory.add_message("user", "Cannot parse message. Please try again.")

    def _get_user_input(self):
        """Get input from the user based on the last message's role."""
        prompt = "What do you want to do? " if not self.memory.get_last_message() else "=> "
        return input(prompt).lower()