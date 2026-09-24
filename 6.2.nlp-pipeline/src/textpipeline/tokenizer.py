"""Tokenizer plugins that create Tokens from document text."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    """One text token represented by its raw string value."""

    value: str

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Tokenizer(ABC):
    """A callable plugin that converts text into Tokens.

    Implementations must raise ``TypeError`` for ``None`` or non-string input.
    They must return an empty list when given an empty string.
    """

    @abstractmethod
    def __call__(self, text: str) -> list[Token]:
        """Tokenize one document's text."""

    @abstractmethod
    def display_name(self) -> str:
        """Return the stable name used to display this plugin."""

    def __repr__(self) -> str:
        return self.display_name()


class WordTokenizer(Tokenizer):
    """Split English words from one document into Tokens. 
    A word is defined as a sequence of word (\\w) characters surrounded by boundaries (\\b). 
    """

    def __call__(self, text: str) -> list[Token]:
        raise NotImplementedError()

    def display_name(self) -> str:
        return "word_tokenizer"
