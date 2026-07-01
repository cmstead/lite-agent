from agent import Agent

agent = Agent({
    "model": "ollama/qwen2.5-coder:14b",
    "api_base": "http://192.168.1.212:11434"
})
agent.run()

