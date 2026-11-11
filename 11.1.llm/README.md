# 11.1 LLM Chat

Use a language model from your terminal through a provider that supports the OpenAI-compatible Chat Completions API. The supplied commands let you send a single prompt with `ask` or hold a conversation with `chat`. This activity verifies that you can access an LLM API and configure a system message.

## Setup

From this activity directory, create and activate a virtual environment and install the project in editable mode.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In PowerShell, activate with `.\.venv\Scripts\Activate.ps1` in place of the `source` command.

Copy `.env.example` to `.env` in this directory. Set `OPENAI_KEY` to your provider's API key and `MODEL` to a model ID available to your account. For a provider other than OpenAI, uncomment `OPENAI_BASE_URL` and set it to the provider's API base URL. Both commands read `.env` from the current directory. Existing environment variables take precedence over the file. Keep your key out of commits and screenshots.

## Run and validate

Run both commands from this directory with the environment active.

```sh
ask "My name is Alex. Greet me by name."
chat
```

Each `ask` invocation sends a fresh request. In `chat`, press Enter to send each message. The command keeps the conversation in memory until you exit with Ctrl+C or EOF. Either command accepts a model override for that invocation, for example `ask --model another-model "Hello"` or `chat --model another-model`. Replace `another-model` with a model ID your provider supports.

Run `sync-assign check 11.1` from the root of your submissions repository. For a local check from this directory, run `python -m pytest`. The test checks the system message without making an API request.

## Student instructions

- **50 points** — Replace `SYSTEM_MESSAGE = None` in `src/chat/cli.py` with a nonempty Python string of your own that tells the model how to respond. Both commands use it as the system message. This is the only code change required.
- **50 points** — Submit a screenshot of your terminal running either command. It must show the message you sent with your own name and the model's reply to that message.
