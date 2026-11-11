"""Terminal clients for the Chat Completions API."""

import os

import click
from dotenv import load_dotenv
from openai import OpenAI

SYSTEM_MESSAGE = None


def create_client(model):
    load_dotenv()
    url = os.environ.get("OPENAI_BASE_URL")
    key = os.environ.get("OPENAI_KEY") or os.environ.get("OPENAI_API_KEY")
    model = model if model is not None else os.environ.get("MODEL", "")
    if not model.strip():
        raise click.UsageError("Set MODEL in .env or pass --model.")
    if not key or not key.strip():
        raise click.UsageError("Set OPENAI_KEY in .env.")

    client = OpenAI(base_url=url, api_key=key.strip())
    click.echo(f"Chatting with {model.strip()} model at {client.base_url}\n", err=True)
    return client, model.strip()


@click.command()
@click.option("--model", help="Override MODEL for this invocation.")
@click.argument("message")
def ask(model, message):
    """Send one message and print the model's reply."""
    if not isinstance(SYSTEM_MESSAGE, str) or not SYSTEM_MESSAGE.strip():
        raise click.UsageError("Set SYSTEM_MESSAGE in src/chat/cli.py before running this command.")
    client, model = create_client(model)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": message},
        ],
    )
    click.echo(response.choices[0].message.content)


@click.command()
@click.option("--model", help="Override MODEL for this invocation.")
def chat(model):
    """Start an interactive conversation."""
    if not isinstance(SYSTEM_MESSAGE, str) or not SYSTEM_MESSAGE.strip():
        raise click.UsageError("Set SYSTEM_MESSAGE in src/chat/cli.py before running this command.")
    client, model = create_client(model)
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    click.echo("Press Ctrl+C or send EOF to exit.")
    while True:
        try:
            message = input("> ")
        except (EOFError, KeyboardInterrupt):
            click.echo()
            break
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(model=model, messages=messages)
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        click.echo(reply)
