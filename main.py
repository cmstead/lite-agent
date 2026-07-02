from agent_core.agent import Agent
from tools import tools

agent = Agent({
    "model": "ollama/qwen2.5-coder:14b",
    "api_base": "http://192.168.1.212:11434"
}, tools)
agent.run()

