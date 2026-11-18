# 12.1 Agent skills for TODO management

An agent skill packages reusable instructions that an AI agent discovers and loads when a request matches its purpose. Implement a skill named `peco` that lets a local AI agent manage TODOs through the [peco application](https://github.com/ludanortmun/peco). The agent must perform real operations in the application and report their results.

## Prerequisites and setup

- Install **peco** before testing this activity. Follow the installation or source-build instructions in the [peco README](https://github.com/ludanortmun/peco#install). This is the TODO application by `ludanortmun`, so verify that you installed the correct executable.
- Make `peco` available on the `PATH` used by your agent. Run `peco --help` to verify installation and inspect the available commands.
- Configure a local AI agent that supports project skills in `.agents/skills/`, a model with tool calling, and a tool that can execute shell commands. Goose is one option; enable its Developer extension for shell access and configure a model provider.
- Open the agent with `12.1.skills/` as its project or working directory. Start a new session after creating or changing the skill if your agent requires it for discovery.

This activity consists of Markdown instructions and an optional shell script; it has no Python dependencies or virtual environment to install. The CLI is sufficient; a running `peco-server` is not required.

## Student work

The template contains an empty file at:

```text
12.1.skills/
├── README.md
└── .agents/
    └── skills/
        └── peco/
            └── SKILL.md
```

Implement `.agents/skills/peco/SKILL.md` yourself. Include YAML frontmatter with `name: peco` and a `description` explaining what the skill does and when to use it, followed by clear Markdown instructions for the agent. The description must support discovery from ordinary TODO and reminder requests, even when the user does not mention peco.

Use the application's documentation and command help to determine the commands and arguments. Your instructions must explain how to obtain needed inputs, execute each operation, verify its outcome, and communicate results. Report command failures accurately rather than claiming success. Use IDs returned by peco; when a description matches multiple TODOs, ask the user which one they mean.

## Required behavior — 100 points

| Action | Required behavior | Points |
|---|---|---:|
| List TODOs | Retrieve actual pending TODOs and show their IDs, content, and due dates when present. Clearly report an empty list. | 30 |
| Create a TODO | Create the requested content, including a due date when supplied, and report the saved TODO and its ID. Resolve relative dates such as “tomorrow” using the current local date and peco's expected date format. A reminder request creates a TODO; it does not schedule a notification. | 40 |
| Mark a TODO as done | Identify the requested existing TODO, mark it completed, and verify its completed state in peco. | 30 |
| **Total** | | **100** |

Each action must work both when the skill is explicitly invoked and when the agent receives a natural-language request without the skill name. Both forms are part of that action's score.

## Run and validate manually

The teacher will grade this activity manually with a local AI agent, inspecting skill loading, tool execution, responses, and the resulting peco data. There is no automated test suite for this activity.

Test all six prompts below in your local AI agent. Slash examples are agent-chat requests, not terminal commands.

| Action | Explicit skill invocation | Natural-language request |
|---|---|---|
| List | `/peco list` | “What do I still need to do?” |
| Create | `/peco create Buy milk from the store, due tomorrow` | “Remind me to get milk from the store by tomorrow.” |
| Done | `/peco done <id>` | “I finished getting milk from the store. Mark that task as done.” |

Replace `<id>` with a real ID from a prior creation or listing. For the two creation tests, use different titles or complete the first TODO before creating the second so that the natural-language completion request identifies one pending task. Test natural-language discovery in a fresh session without explicitly loading `peco` first.

Check the underlying application after each operation. Use `peco list` to verify pending items and `peco list --include-done` to verify completed items. Confirm that both creation prompts save the requested content and tomorrow's local calendar date, and that completion changes the intended TODO's state. Also test listing when there are no pending TODOs. Use test TODOs you can recognize.

## Extra credit — 10 points

Add `.agents/skills/peco/setup.sh` that ensures the correct peco application is installed and available to the agent. It must detect an existing installation, install peco when missing using the project's documented installation method for your supported platform, and verify that the executable works afterward. Repeated runs must succeed without unnecessary reinstallation. Report installation failures with a nonzero exit status. Document the supported platform and how to run the script in your skill, and explain when the agent should use it.

See [Goose: using skills and supporting files](https://goose-docs.ai/docs/guides/context-engineering/using-skills/) for organizing a skill with a setup script. The teacher will review and run the script to verify this extra credit; the base activity assumes peco is already installed.

Submit the completed `SKILL.md` and, if attempted, `setup.sh` inside this activity directory. Keep local databases and installed executables out of the submission.
