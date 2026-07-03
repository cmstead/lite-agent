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

class QuestionAction:
    def execute(self, args):
        return input(f"{args[0] if args else 'Question'}: ")

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
        "question", 
        ["question"], 
        "Use this to ask a question to the user and get their input.", 
        QuestionAction()
    ),

    Tool(
        "terminate", 
        ["message"], 
        "Use this to end the agent process.", 
        TerminateAction()
    ),
]