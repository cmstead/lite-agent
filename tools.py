import subprocess
from agent_core.tool import Tool

class TerminalAction:
    def execute(self, args):
        print(f"Allow action {args[0]}?")
        user_input = input("Type 'yes' to allow, 'no' to disallow: ")
        if user_input.lower() == 'yes' or user_input.lower() == 'y':
            return subprocess.run(args[0].split(' '), capture_output=True, text=True)
        else:
            return "Action cancelled by user."

tools = [
    Tool(
        "terminal", 
        ["command to execute"], 
        "Use this to execute terminal commands.", 
        TerminalAction()
    ),
]