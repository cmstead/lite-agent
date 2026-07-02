import subprocess
from tool import Tool

class TerminalAction:
    def execute(self, args):
        print(f"Allow action {args[0]}?")
        user_input = input("Type 'yes' to allow, 'no' to disallow: ")
        if user_input.lower() == 'yes' or user_input.lower() == 'y':
            return subprocess.run(args[0].split(' '), capture_output=True, text=True)
        else:
            return "Action cancelled by user."

class ListAction:
    def execute(self, args):
        for item in args:
            print(f"- {item}")

class MessageAction:
    def execute(self, args):
        for message in args:
            print(f"{message}")

class RequestAction:
    def execute(self, args):
        for request in args:
            print(f"Making request: {request}")

class TerminateAction:
    def execute(self):
        # Implementation for terminating the process
        pass

tools = [
    Tool(
        "terminal", 
        ["command to execute"], 
        "Use this to execute terminal commands.", 
        TerminalAction()
    ),

    Tool(
        "list", 
        ["options"], 
        "Use this to present a list of options to the user.", 
        ListAction()
    ),

    Tool(
        "message", 
        ["message"], 
        "Use this to send a message to the user.", 
        MessageAction()
    ),

    Tool(
        "request", 
        ["message"], 
        "Use this for requests to the user.", 
        RequestAction()
    ),

    Tool(
        "terminate", 
        [], 
        "Use this to end the agent process.", 
        TerminateAction()
    ),
]