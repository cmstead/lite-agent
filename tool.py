class Tool:
    def __init__(self, name, arguments, description, action):
        self.name = name
        self.arguments = arguments
        self.description = description
        self.action = action

    def to_dict(self):
        return {
            "name": self.name,
            "arguments": self.arguments,
            "description": self.description,
        }
    
    def execute(self, args):
        return self.action.execute(args)