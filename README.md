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
  - `Memory` keeps only the most recent 10 messages (including the system-injected tool results), so long-running sessions lose earlier context.
  - Typing `/bye` at the input prompt exits the loop; `/clear` wipes memory without exiting.
  - Calling the `terminate` tool also clears memory and ends the current exchange (the loop then prompts again for new input).
- `agent_core/tool.py` — `Tool`: a simple `(name, arguments, description, action)` wrapper. `action` is any object with an `execute(args)` method.
- `agent_core/tool_utils.py` — parses the ` ```tool ` fenced JSON block out of a model response (`parse_tool_response`) and prints the tool's `message`/`description` to the user (`print_tool_message`).
- `agent_core/system_message.py` — builds the system prompt: injects the agent prompt, a note that the agent should not perform destructive actions (deleting files, hacking remote systems), the current OS/Python version, the required ` ```tool ` response format, an instruction to plan step by step before acting, and the tool catalog.
- `agent_core/core_tools.py` — built-in tools always available to the agent:
  - `choose` — presents a list of options to the user and returns their selection (via `inquirer`).
  - `confirm` — asks the user a Yes/No confirmation question.
  - `message` — prints one or more message lines to the user.
  - `plan` — prints a checklist of plan steps (used to make the model think step by step before acting).
  - `question` — asks the user a free-text question and returns their answer.
  - `terminate` — ends the agent loop.
- `tools.py` — project-specific tools passed in alongside the core tools:
  - `code` — prints a code snippet in a fenced block.
  - `http` — performs an HTTP GET request against a URL and returns the response body.
  - `instructions` — Reads instructions from `~/.instructions/<name>-instructions.md` and executes them
  - `read_file` — reads a file and returns its contents.
  - `write_file` — writes content to a file.
  - `terminal` — runs a shell command. `cat`/`ls` commands run without confirmation; everything else prompts the user to confirm (`yes`/`no`) via `inquirer` before running; `cat *` is explicitly rejected.
- `main.py` — entry point: loads `OPENAI_API_KEY` (or other provider credentials) from a `.env` file via `python-dotenv`, joins any CLI arguments into an initial message, wires up an `Agent` with a model config, the tool list, an agent system prompt, and the initial message, then calls `agent.run()`.

## Requirements

- Python 3.13
- An LLM endpoint reachable by LiteLLM
- A `.env` file in the project root with the credentials your chosen provider needs, e.g. `OPENAI_API_KEY=...` (loaded via `python-dotenv`; `.env` is gitignored)

Install dependencies:

```bash
source .venv/bin/activate
pip install -r Requirements.txt
```

## Usage

Edit the model config and agent prompt in `main.py` to point at your LLM provider/endpoint:

```python
agent = Agent({
        # "model": "ollama/qwen2.5-coder:14b",
        # "api_base": "http://192.168.1.212:11434"
        "model": "gpt-4o-mini",
    },
    tools,
    "You are a helpful technical and coding agent ...",
    ' '.join(args) if len(args) > 0 else None
)
```

Then run:

```bash
python main.py
```

Any command-line arguments are joined together and queued as the agent's first user message; otherwise you'll be prompted with `What do you want to do?`. The agent will respond by invoking tools (asking questions, printing messages, running terminal commands) until it calls `terminate`. Type `/bye` at any prompt to exit, or `/clear` to reset the conversation memory without exiting.

## Adding a new tool

1. Define a class with an `execute(args)` method that performs the action and returns a result (or `None`).
2. Wrap it in a `Tool(name, arguments, description, action)`.
3. Add it to the `tools` list in `tools.py` (or pass your own list into `Agent(...)`).

The tool's `name`, `arguments`, and `description` are automatically included in the system prompt so the model knows it's available and how to call it.

## Notes

- The `terminal` tool asks for interactive confirmation (`yes`/`no`) before running most commands — it does not sandbox or validate the command otherwise, so treat it as trusted-user tooling only.
- The `read_file`, `write_file`, and `http` tools have no path/URL validation or sandboxing — they operate with the permissions of the running process.
- Model responses that don't follow the ` ```tool ` fenced format are printed as-is and treated as having no tool call.
- Conversation memory is capped at the last 10 messages, so very long sessions will lose earlier context.
