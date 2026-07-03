import inquirer
from agent_core.tool import Tool

class ChooseAction:
    def execute(self, args):
        print(args)
        if not args or len(args) == 0:
            print("No options provided.")
            return None
        
        prompts = [inquirer.List(
            'choice',
            message="Please choose from the following:",
            choices=args
        )]

        responses = inquirer.prompt(prompts)
        return responses['choice'] if responses else None

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
        "choose", 
        ["options"], 
        "Use this to present a list of options to the user.", 
        ChooseAction()
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