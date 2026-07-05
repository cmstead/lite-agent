import re
import subprocess
import inquirer
from agent_core.tool import Tool

class TerminalAction:
    def execute(self, args):
        if args[0] == "cat *":
            return "`cat *` is not a valid command."
            
        if re.match(r'^(cat|ls)', args[0]):
            print(f"Executing `{args[0]}` ...")
            return subprocess.run(args[0].split(' '), capture_output=True, text=True)
        
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

class ReadFileAction:
    def execute(self, args):
        print(f"Reading {args[0]} ...")
        try:
            with open(args[0], 'r') as file:
                content = file.read()
                return content[:4000]
        except Exception as e:
            return f"Error reading file: {e}"

class WriteFileAction:
    def execute(self, args):
        print(f"Writing to {args[0]} ...")
        try:
            with open(args[0], 'w') as file:
                file.write(args[1])
                return f"Successfully wrote to {args[0]}"
        except Exception as e:
            return f"Error writing to file: {e}"

class CodeAction:
    def execute(self, args):
        print(f"```code\n{args[0]}\n```")
        return "Code displayed successfully."

class HttpAction:
    def execute(self, args):
        import requests
        print(f"Fetching {args[0]} ...")
        response = requests.get(args[0])
        return response.text[:4000]

tools = [
    Tool(
        "code", 
        ["code to display"], 
        "Use this to display code snippets.", 
        CodeAction()
    ),
    Tool(
        "http", 
        ["url to request"], 
        "Use this to make HTTP GET requests.", 
        HttpAction()
    ),
    Tool(
        "read_file", 
        ["file path"], 
        "Use this to read the contents of a file.", 
        ReadFileAction()
    ),
    Tool(
        "write_file", 
        ["file path", "content to write"], 
        "Use this to write content to a file.", 
        WriteFileAction()
    ),
    Tool(
        "terminal", 
        ["command to execute"], 
        "Use this to execute terminal commands.", 
        TerminalAction()
    ),
]