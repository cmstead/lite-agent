import inquirer
from agent_core.tool import Tool

class ChooseAction:
    def execute(self, args):
        if not args or len(args) == 0:
            print("No options provided.")
            return None
        
        splitArgs = args[0].split(" ")
        choices = splitArgs if len(splitArgs) > 1 else args

        prompts = [inquirer.List(
            'choice',
            message="Please choose from the following:",
            choices=choices
        )]

        responses = inquirer.prompt(prompts)
        return responses['choice'] if responses else None

class ConfirmAction:
    def execute(self, args):
        if not args or len(args) == 0:
            print("No confirmation message provided.")
            return None
        
        prompts = [inquirer.List(
            'confirmation',
            message=args[0],
            choices=["Yes", "No"]
        )]

        responses = inquirer.prompt(prompts)
        return responses['confirmation'] if responses else None

class HelpAction:
    def execute(self, args):
        print("Type whatever you want to do and I will try to help you. You can also use the following commands:")
        print("Type /clear to clear and start a new chat.")
        print("Type /exit to exit the program.")
        return "Help message displayed. Return control to user prompt."

class QuestionAction:
    def execute(self, args):
        return input(f"{args[0] if args else 'Question'}: ")

class MessageAction:
    def execute(self, args):
        if not args or len(args) == 0:
            return "No message data available. Message body is empty. Return control to user prompt."
        for arg in args:
            print(f"{arg}")
        
        return "Message displayed successfully. Return control to user prompt."
    
class PlanAction:
    def execute(self, args):
        print("Plan:")
        for step in args:
            print(f"-[] {step}")
        return "Execute plan"

class TerminateAction:
    def execute(self, args):
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
        "confirm", 
        ["message"], 
        "Use this to ask the user for confirmation (Yes/No).", 
        ConfirmAction()
    ),

    Tool(
        "help", 
        [], 
        "Use this to display a help message with available tools.", 
        HelpAction()
    ),

    Tool(
        "message", 
        ["message_lines"], 
        "Use this to display a message to the user.", 
        MessageAction()
    ),

    Tool(
        "plan",
        ["plan steps"],
        "Use this to think step by step and build a plan",
        PlanAction()
    ),

    Tool(
        "question", 
        ["question"], 
        "Use this to ask a question to the user and get their input.", 
        QuestionAction()
    ),

    Tool(
        "terminate", 
        [], 
        "Use this to end the agent process.", 
        TerminateAction()
    ),
]