# lite-agent

A minimal, hackable LLM agent loop written in Python. It talks to any model supported by [LiteLLM](https://github.com/BerriAI/litellm) (OpenAI, Ollama, Anthropic, etc.), drives a simple JSON tool-call protocol, and ships with a small set of tools for interacting with the user, the terminal, and the web.

## How it works

The agent runs a read-eval-print loop:

1. Prompt the user for input (unless the last turn already queued a tool result).
2. Send the full conversation, plus a system message describing available tools, to the model via `litellm.completion`.
3. Parse the model's reply as a fenced ` ```tool ` JSON block containing `name`, `message`, and `arguments`.
4. Look up the named tool and execute it, feeding the result back into the conversation as the next user turn.
5. Repeat until the model calls the `terminate` tool.

### Core pieces

- `agent_core/agent.py` — `Agent` and `Memory` classes: the main loop, message history, and dispatch to tools.
- `agent_core/tool.py` — `Tool`: a simple `(name, arguments, description, action)` wrapper. `action` is any object with an `execute(args)` method.
- `agent_core/tool_utils.py` — parses the ` ```tool ` fenced JSON block out of a model response.
- `agent_core/system_message.py` — builds the system prompt, injecting the tool catalog and response format instructions.
- `agent_core/core_tools.py` — built-in tools always available to the agent:
  - `choose` — presents a list of options to the user and returns their selection (via `inquirer`).
  - `message` — prints a message to the user.
  - `terminate` — ends the agent loop.
- `tools.py` — project-specific tools passed in alongside the core tools:
  - `terminal` — runs a shell command, after prompting the user to confirm.
- `main.py` — entry point that wires up an `Agent` with a model config and the tool list, then calls `agent.run()`.

## Requirements

- Python 3.13
- An LLM endpoint reachable by LiteLLM — the default config in `main.py` points at a local Ollama server

Install dependencies:

```bash
source .venv/bin/activate
pip install -r Requirements.txt
```

## Usage

Edit the model config in `main.py` to point at your LLM provider/endpoint:

```python
agent = Agent({
    "model": "ollama/qwen2.5-coder:14b",
    "api_base": "http://192.168.1.212:11434"
}, tools)
```

Then run:

```bash
python main.py
```

You'll be prompted with `What do you want to do?`. The agent will respond by invoking tools (asking questions, printing messages, running terminal commands) until it calls `terminate`.

## Adding a new tool

1. Define a class with an `execute(args)` method that performs the action and returns a result (or `None`).
2. Wrap it in a `Tool(name, arguments, description, action)`.
3. Add it to the `tools` list in `tools.py` (or pass your own list into `Agent(...)`).

The tool's `name`, `arguments`, and `description` are automatically included in the system prompt so the model knows it's available and how to call it.

## Notes

- The `terminal` tool asks for interactive confirmation (`yes`/`no`) before running any command — it does not sandbox or validate the command otherwise, so treat it as trusted-user tooling only.
- The `http` tool allows the agent to perform HTTP GET requests to specified URLs, facilitating data retrieval from web resources.
- Model responses that don't follow the ` ```tool ` fenced format are printed as-is and treated as having no tool call.
