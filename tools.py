from tool import Tool

class TerminalAction:
    def execute(self, command):
        # Implementation for executing a terminal command
        pass

class ListAction:
    def execute(self, options):
        # Implementation for presenting a list of options
        pass

class MessageAction:
    def execute(self, message):
        # Implementation for sending a message
        pass

class RequestAction:
    def execute(self, message):
        # Implementation for making a request
        pass

class TerminateAction:
    def execute(self):
        # Implementation for terminating the process
        pass

tools = [
    Tool(
        "Terminal", 
        ["command to execute"], 
        "Use this to execute terminal commands.", 
        TerminalAction()
    ),
    
    Tool(
        "List", 
        ["options"], 
        "Use this to present a list of options to the user.", 
        ListAction()
    ),

    Tool(
        "Message", 
        ["message"], 
        "Use this to send a message to the user.", 
        MessageAction()
    ),

    Tool(
        "Request", 
        ["message"], 
        "Use this for requests to the user.", 
        RequestAction()
    ),

    Tool(
        "Terminate", 
        [], 
        "Use this to end the agent process.", 
        TerminateAction()
    ),
]