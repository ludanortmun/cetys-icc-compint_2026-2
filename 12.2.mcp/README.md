# 12.2 MCP for peco

Build an MCP server that lets AI agents list, create, edit, and complete TODOs in [peco](https://github.com/ludanortmun/peco). Use **FastMCP** and **stdio** to expose these operations as executable tools, then connect them to a supplied terminal chat using Chat Completions.

The server must work independently of the supplied chat with any agent application supporting stdio MCP, such as Goose, Codex, or Claude Code. The chat is a purpose-built peco agent: it connects to this server only. You do not need a server registry, configurable transports, or support for other MCP servers.

## Setup

Use **Python 3.14**. From this activity directory:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Ensure `python` selects Python 3.14 before creating the environment. On PowerShell, activate with `.\.venv\Scripts\Activate.ps1` instead.

Install the correct **peco TODO application by ludanortmun**, following its [installation instructions](https://github.com/ludanortmun/peco#install), and make `peco` available on the server process's `PATH`. Verify the interface:

```sh
peco --help
peco new --help
peco list --help
peco edit --help
peco complete --help
```

Use the CLI; you do not need to start `peco-server`. Its local database persists between sessions. Use recognizable test tasks. Keep databases, executables, `.env`, and virtual environments out of your submission.

For the chat, copy `.env.example` to `.env` in this directory. Set `OPENAI_KEY` (or `OPENAI_API_KEY`) and `MODEL` for a provider supporting OpenAI-compatible **Chat Completions with tool calling**. Optionally set `OPENAI_BASE_URL`. Existing environment variables take precedence. The MCP server itself does not use an LLM, credentials, or `.env`.

## Supplied scaffold

```text
12.2.mcp/
├── README.md
├── .env.example
├── pyproject.toml
├── requirements.txt
├── src/peco_agent/
│   ├── __init__.py
│   ├── server.py
│   ├── client.py
│   └── chat.py
└── tests/
```

`chat.py` supplies the terminal loop, conversation history, model calls, tool-calling rounds, and a system prompt dedicated to peco. The supplied `async with Client(server) as mcp:` block opens the stdio connection, closes it on exit, and keeps one MCP session open for the conversation. The chat handles several calls per model response and successive tool rounds. Leave this infrastructure and its prompt intact. Implement the six stubs in `server.py` and `client.py`; you may add helpers in those modules. Preserve their signatures and the supplied tests.

## MCP server — 70 points

`server.py` supplies the FastMCP instance, typed tool signatures, tool decorators, and stdio entry point. Implement the four bodies using the actual peco CLI. Return captured stdout as a string, including the generated ID for changes. An empty list may return peco's header without rows. Do not fabricate records or maintain a separate TODO store.

| Tool | Required behavior | Points |
|---|---|---:|
| `list_todos(include_done=False)` | Run `peco list`; include `--include-done` when requested. Return IDs, states, due dates, and content, including the empty case. | 20 |
| `create_todo(content, due=None)` | Run `peco new` with the requested content and optional `--due` date; return the creation result and assigned ID. | 20 |
| `edit_todo(todo_id, content=None, due=None)` | Run `peco edit` for the existing ID with only the supplied fields. Preserve omitted fields and the task's state. | 15 |
| `complete_todo(todo_id)` | Run `peco complete` for the existing ID and return its result. Affect only that task. | 15 |
| **Server subtotal** | | **70** |

Pass CLI arguments as a list using `subprocess.run` with captured text output and failure checking, without a shell. Content containing spaces, quotes, or shell characters must remain one literal argument. Dates use local `YYYY-MM-DD`; omit date flags for `None`. Editing supports replacement of content and/or due date; clearing a due date is outside this activity. IDs come from peco. Do not print CLI output to the server's stdout: stdio reserves it for MCP. Let CLI failures become MCP tool errors rather than returning success text. FastMCP handles schemas, initialization, and protocol messages.

## MCP client integration — 30 points

Implement the following methods in `client.py`. The chat already calls them at the appropriate places; no extensible host framework is required.

| Method | Required behavior | Points |
|---|---|---:|
| `discover_tools(mcp)` | Await `list_tools()` and adapt the peco tools to Chat Completions function definitions. Preserve each tool's name, description (or `""`), and input schema as `parameters`. Obtain definitions from MCP rather than duplicating schemas in the chat. | 15 |
| `execute_tool(mcp, call)` | Decode `call.function.arguments` from JSON, await `call_tool(name, arguments)`, and return a tool message associated with `call.id`. Serialize `{"result": result.data}` on success. On malformed JSON or a failed MCP call, return `{"error": "a nonempty explanation"}` so the model receives the failure and can respond. | 15 |
| **Client subtotal** | | **30** |
| **Assignment total** | | **100** |

A tool result message has `role: "tool"`, `tool_call_id: call.id`, and `content` containing a JSON **string**. Preserve every call's identifier. The supplied `reply()` appends these messages after the assistant's tool request and sends the updated history back to the model until it replies with text.

See [FastMCP client lifecycle](https://gofastmcp.com/docs/clients/client), [stdio transports](https://gofastmcp.com/docs/clients/transports), and [tool discovery and execution](https://gofastmcp.com/docs/clients/tools). Use the standalone `fastmcp` package.

## Run and validate

After implementing the stubs, run from this activity directory with the environment active:

```sh
python -m pytest
python -m peco_agent.chat
```

Type `/exit`, send EOF, or press Ctrl+C to exit. The chat starts and closes the server; do not launch a second server for it. Try this conversation, substituting a real ID when needed:

1. “What do I still need to do?”
2. “Remind me to buy milk tomorrow.”
3. “Change that task to buy milk and coffee, due the day after tomorrow.”
4. “I bought the milk and coffee. Mark that task as done.”
5. “Show all tasks, including completed ones.”

Verify actual data with `peco list` and `peco list --include-done`. Check content, IDs, dates, and completed state. Test an empty list, omitted edit fields, and a nonexistent ID. If several tasks match a description, the supplied prompt tells the agent to ask which one. These behaviors exercise the same scored tools and client methods.

The automated tests run a controlled peco replacement through real stdio MCP subprocesses and simulate model responses. They require no installed peco, API key, paid API requests, or personal database access. They cover the six scored functionalities, including literal content, preservation of omitted fields, error propagation, schema adaptation, result IDs, and multiple tool calls and rounds. The controlled executable fixture requires a POSIX environment (macOS or Linux; use WSL on Windows). They do not substitute for trying the finished agent with actual peco and your model.

Run the canonical validation from the root of your submissions repository:

```sh
sync-assign check 12.2
```

## Use the server in another agent application

Configure a **stdio MCP server** in your host. Supply absolute paths to this activity's virtual-environment Python and the server script; the host must be able to find `peco` on its `PATH`.

```text
Command: /absolute/path/12.2.mcp/.venv/bin/python
Arguments: /absolute/path/12.2.mcp/src/peco_agent/server.py
```

On Windows, the interpreter is `.venv\Scripts\python.exe`. If the application accepts a single command field, combine and quote the paths as needed. If it accepts MCP JSON configuration, adapt these placeholder paths:

```json
{
  "mcpServers": {
    "peco": {
      "command": "/absolute/path/12.2.mcp/.venv/bin/python",
      "args": ["/absolute/path/12.2.mcp/src/peco_agent/server.py"]
    }
  }
}
```

Goose offers a Standard IO custom extension; other hosts may use their own configuration format. The executable and arguments above stay the same. The host launches the server; it does not run `chat.py`. No HTTP URL, port, model configuration, or skill is needed for the MCP connection. In that host, discover all four tools and ask it to list, create, edit, and complete a recognizable test task. Inspect actual tool calls and verify the saved peco data. The server's tools must work without importing or depending on the terminal chat.

Submit the completed activity directory, including the unchanged scaffold and tests. No extra credit is defined.
