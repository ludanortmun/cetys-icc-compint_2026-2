"""Supplied demonstration CLI; not graded."""

from pathlib import Path
from tempfile import gettempdir

import click

from . import Document, VectorStore


def make_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2", device="cpu",
        cache_folder=str(Path(gettempdir()) / "compint" / "10.2.vector-store"),
    )


@click.group()
def cli():
    """Try the vector store (requires the persistence extra credit)."""


@cli.command()
@click.option("--path", type=click.Path(path_type=Path, dir_okay=False), required=True)
@click.option("--text", required=True, help="Document text.")
@click.option("--tag", multiple=True, help="Repeat for multiple metadata tags.")
def add(path, text, tag):
    """Append one document, creating the store file if needed."""
    model = make_model()
    store = VectorStore.load(path, model) if path.exists() else VectorStore(model)
    store.add([Document(text, set(tag))])
    store.save(path)
    click.echo(f"Added document to {path}")


@cli.command()
@click.option("--path", type=click.Path(path_type=Path, exists=True, dir_okay=False), required=True)
@click.option("--query", required=True)
@click.option("--k", default=3, type=click.IntRange(min=1), show_default=True)
@click.option("--tag", multiple=True, help="Require every supplied tag.")
def search(path, query, k, tag):
    """Load a store and print its most similar documents."""
    store = VectorStore.load(path, make_model())
    for document, score in store.search(query, k=k, metadata=set(tag)):
        click.echo(f"{score:.6f}\t{document.text}\t{sorted(document.metadata)}")


if __name__ == "__main__":
    try:
        cli()
    except NotImplementedError:
        raise click.ClickException("Complete Document, VectorStore, and persistence first.")
