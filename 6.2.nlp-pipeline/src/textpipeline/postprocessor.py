"""Postprocessor plugins that transform document Tokens."""

from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import gettempdir

import nltk
from nltk.stem import WordNetLemmatizer

from textpipeline.tokenizer import Token


class Postprocessor(ABC):
    """A callable plugin that transforms a document's Tokens.

    Implementations must raise ``TypeError`` for ``None`` or non-list input.
    They must return an empty list when given an empty token list.
    """

    @abstractmethod
    def __call__(self, tokens: list[Token]) -> list[Token]:
        """Transform one document's Tokens."""

    @abstractmethod
    def display_name(self) -> str:
        """Return the stable name used to display this plugin."""

    def __repr__(self) -> str:
        return self.display_name()

ENGLISH_STOPWORDS = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "but", "by", "for",
        "from", "has", "he", "i", "in", "is", "it", "its", "of", "on",
        "or", "that", "the", "this", "to", "was", "we", "with", "you",
    }
)


class SimpleStemmer(Postprocessor):
    """Remove simple ``ing``, ``ed``, and ``s`` suffixes from Tokens."""

    def __call__(self, tokens: list[Token]) -> list[Token]:
        raise NotImplementedError()

    def display_name(self) -> str:
        return "simple_stemmer"


class StopwordRemover(Postprocessor):
    """Remove Tokens included in the supplied English stopword set."""

    def __call__(self, tokens: list[Token]) -> list[Token]:
        raise NotImplementedError()

    def display_name(self) -> str:
        return "stopword_remover"


class Lemmatizer(Postprocessor):
    """Lemmatize Tokens with NLTK WordNet using this instance's POS tag."""

    def __init__(self, pos: str = "n") -> None:
        self.pos = pos
        self.lemmatizer = WordNetLemmatizer()

    def ensure_wordnet(self) -> None:
        """Make the WordNet corpus available in this temporary session."""
        data_dir = Path(gettempdir()) / "textpipeline_nltk_data"
        data_dir.mkdir(parents=True, exist_ok=True)

        if str(data_dir) not in nltk.data.path:
            nltk.data.path.insert(0, str(data_dir))

        try:
            nltk.data.find("corpora/wordnet")
        except LookupError:
            nltk.download(
                "wordnet",
                download_dir=str(data_dir),
                quiet=True,
                raise_on_error=True,
            )

    def __call__(self, tokens: list[Token]) -> list[Token]:
        raise NotImplementedError()

    def display_name(self) -> str:
        return f"lemmatizer(pos={self.pos})"


class NGramGenerator(Postprocessor):
    """Generate Tokens by joining n consecutive Tokens with ``<sep>``."""

    def __init__(self, n: int) -> None:
        self.n = n

    def __call__(self, tokens: list[Token]) -> list[Token]:
        raise NotImplementedError()

    def display_name(self) -> str:
        return f"ngram_generator(n={self.n})"
