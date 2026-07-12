class Memory:
    def __init__(self):
        self.messages = []

    def clear(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-10:]
    
    def get_messages(self):
        return self.messages

    def get_last_message(self):
        return self.messages[-1] if self.messages else None
    
    def get_last_two_agent_messages(self):
        agent_messages = []
        message_length = len(self.messages)
        index = -1

        while message_length + index > 0 and len(agent_messages) < 2:
            if self.messages[index].get("role") == "assistant":
                agent_messages.append(self.messages[index].get("content"))
            index -= 1

        return agent_messages

