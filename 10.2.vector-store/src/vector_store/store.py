"""Student contracts. Implement every required method without changing signatures."""

from os import PathLike
from typing import Protocol

import numpy as np


class Encoder(Protocol):
    """Subset of SentenceTransformer used by the store; supplied, unscored."""

    def encode(self, sentences: list[str], *, convert_to_numpy: bool = True,
               normalize_embeddings: bool = False) -> np.ndarray: ...


class Document:
    """Text and optional arbitrary, case-sensitive string tags (not embedded).

    Public attributes: text: str; metadata: set[str]. Copy input tags; None
    means a fresh empty set. Inputs have the annotated types; no validation
    or equality/hash implementation is required. Preserve text verbatim.
    """

    def __init__(self, text: str, metadata: set[str] | None = None) -> None:
        raise NotImplementedError


class VectorStore:
    """Keep documents and NumPy embeddings aligned in insertion order.

    Accept a supplied SentenceTransformer-compatible encoder. Do not load a
    model here. Internal storage is your choice; tests use only public methods.
    """

    def __init__(self, model: Encoder) -> None:
        """Create an independent empty store using model; do not encode yet."""
        raise NotImplementedError

    def add(self, documents: list[Document]) -> None:
        """Append documents and encode only their text, keeping duplicate entries.

        Use model.encode(list_of_texts, convert_to_numpy=True,
        normalize_embeddings=False). Keep embeddings for subsequent queries;
        never re-encode stored documents during search. Empty input is a no-op.
        Model outputs are finite 2D arrays with a consistent positive dimension.
        Documents will not be mutated after insertion.
        """
        raise NotImplementedError

    def search(self, query: str, k: int = 3,
               metadata: set[str] | None = None) -> list[tuple[Document, float]]:
        """Return at most k (document, cosine_score) pairs, highest score first.

        Encode [query] using the same kwargs as add; calculate cosine (util.cos_sim is allowed).
        Define cosine as zero if either vector has zero norm. Keep negative
        scores and insertion order for exact ties; do not round before sorting.
        Require ALL query tags (subset match), case-sensitive; None/empty means
        no filter. Filter before top-k. Empty store/no matches returns [].
        k <= 0 raises ValueError, even on an empty store. k is an integer.
        """
        raise NotImplementedError

    def save(self, path: str | PathLike[str]) -> None:
        """Extra credit: write text, tags, order, and embeddings to this file.

        Overwrite an existing file. Do not append an extension or serialize the
        model. Format is your choice. Parent directory already exists.
        """
        raise NotImplementedError

    @classmethod
    def load(cls, path: str | PathLike[str], model: Encoder) -> "VectorStore":
        """Extra credit: return an independent store from the explicit file path.

        Restore embeddings without re-encoding documents. The caller supplies
        the same model/configuration used when saving. Support empty stores and
        subsequent add/search/save; missing files raise FileNotFoundError.
        """
        raise NotImplementedError
