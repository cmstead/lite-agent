import sys
import dotenv
from agent_core.agent import Agent
from tools import tools

args = sys.argv[1:]

dotenv.load_dotenv()

agent = Agent({
        # "model": "ollama/qwen3.5:9b",
        # "api_base": "http://192.168.1.212:11434"
        "model": "gpt-4o",
    }, 
    tools,
    "You are a helpful personal technical assistant. You will be given a task to complete. You will be provided with tools to help you complete the task. You should use the tools to complete the task. You should not make up information. If you are unsure about something, you should ask for clarification.",
    ' '.join(args) if len(args) > 0 else None
)
agent.run()
