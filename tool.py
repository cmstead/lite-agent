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
    
    def execute(self, *args):
        if len(args) != len(self.arguments):
            raise ValueError(f"Expected {len(self.arguments)} arguments, got {len(args)}")
        return self.action.execute(*args)