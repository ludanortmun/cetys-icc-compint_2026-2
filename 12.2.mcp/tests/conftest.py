"""Controlled peco executable: real stdio MCP, no personal database or LLM API."""
import copy
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
import pytest

SERVER = Path(__file__).parents[1] / "src/peco_agent/server.py"

FAKE_PECO = r'''import json
import os
from pathlib import Path
import sys

path = Path(os.environ["TEST_PECO_DB"])
items = json.loads(path.read_text())
args = sys.argv[1:]
with Path(os.environ["TEST_PECO_LOG"]).open("a") as log:
    log.write(json.dumps(args) + "\n")

def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)

def flags(arguments):
    result = {}
    while arguments:
        flag = arguments.pop(0)
        if not flag.startswith("--"):
            fail("unexpected argument")
        if "=" in flag:
            key, value = flag.split("=", 1)
        else:
            key, value = flag, arguments.pop(0)
        result[key] = value
    return result

command = args.pop(0)
if command == "list":
    if args not in ([], ["--include-done"]):
        fail("invalid list arguments")
    print("ID  STATE  DUE  CONTENT")
    for item in items:
        if item["state"] == "pending" or args:
            print(f'{item["id"]}  {item["state"]}  {item["due"] or "-"}  {item["content"]}')
elif command == "new":
    content = args.pop(0)
    options = flags(args)
    if not content.strip():
        fail("content must not be empty")
    item = dict(id=max([i["id"] for i in items], default=0)+1,
                content=content, due=options.get("--due"), state="pending")
    items.append(item)
    print(f'Created todo {item["id"]}')
elif command in ("edit", "complete"):
    identifier = int(args.pop(0))
    item = next((i for i in items if i["id"] == identifier), None)
    if item is None:
        fail("todo not found")
    if command == "complete":
        if args:
            fail("unexpected argument")
        item["state"] = "done"
        print(f'Completed todo {identifier}')
    else:
        options = flags(args)
        if "--content" in options:
            if not options["--content"].strip():
                fail("content must not be empty")
            item["content"] = options["--content"]
        if "--due" in options:
            item["due"] = options["--due"]
        print(f'Updated todo {identifier}')
else:
    fail("unknown command")
path.write_text(json.dumps(items))
'''


@pytest.fixture
def peco_env(tmp_path, monkeypatch):
    executable = tmp_path / "peco"
    executable.write_text(f"#!{sys.executable}\n" + FAKE_PECO)
    executable.chmod(0o755)
    database = tmp_path / "todos.json"
    database.write_text("[]")
    log = tmp_path / "calls.jsonl"
    log.touch()
    monkeypatch.setenv("PATH", str(tmp_path) + os.pathsep + os.environ["PATH"])
    monkeypatch.setenv("TEST_PECO_DB", str(database))
    monkeypatch.setenv("TEST_PECO_LOG", str(log))
    return SimpleNamespace(
        seed=lambda items: database.write_text(json.dumps(items)),
        read=lambda: json.loads(database.read_text()),
        calls=lambda: [json.loads(line) for line in log.read_text().splitlines()],
        env=dict(os.environ),
    )


@pytest.fixture
async def mcp(peco_env):
    transport = PythonStdioTransport(SERVER, python_cmd=sys.executable, env=peco_env.env)
    async with Client(transport) as client:
        yield client


def todo(identifier=7, content="Read chapter", due="2026-12-01", state="pending"):
    return dict(id=identifier, content=content, due=due, state=state)


class Model:
    def __init__(self, *messages):
        self.messages = iter(messages)
        self.requests = []
        self.chat = SimpleNamespace(completions=self)

    def create(self, **request):
        self.requests.append(copy.deepcopy(request))
        return SimpleNamespace(choices=[SimpleNamespace(message=next(self.messages))])
