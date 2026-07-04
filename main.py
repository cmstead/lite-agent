import dotenv
from agent_core.agent import Agent
from tools import tools

dotenv.load_dotenv()

agent = Agent({
    "model": "ollama/qwen2.5-coder:14b",
    "api_base": "http://192.168.1.212:11434"
}, 
tools,
"You are a helpful technical and coding agent that can assist with programming tasks, code generation, debugging, and providing explanations for code snippets. You can also help with algorithm design, data structures, and best practices in software development. Please provide clear and concise responses to coding-related queries."
)
agent.run()

