import subprocess
import inquirer
from agent_core.tool import Tool

class TerminalAction:
    def execute(self, args):
        questions = [
            inquirer.List('confirm',
                        message=f"Allow action `{args[0]}`?",
                        choices=['yes', 'no'],
                        default='yes'),
        ]
        answers = inquirer.prompt(questions)
        if answers['confirm'] == 'yes':
            return subprocess.run(args[0].split(' '), capture_output=True, text=True)
        else:
            return "Action cancelled by user."

class CodeAction:
    def execute(self, args):
        print(f"```code\n{args[0]}\n```")
        return "Code displayed successfully."

tools = [
    Tool(
        "code", 
        ["code to display"], 
        "Use this to display code snippets.", 
        CodeAction()
    ),
    Tool(
        "terminal", 
        ["command to execute"], 
        "Use this to execute terminal commands.", 
        TerminalAction()
    ),
]