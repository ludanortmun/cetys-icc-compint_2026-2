"""Preprocessor plugins that transform raw document text."""

from abc import ABC, abstractmethod


class Preprocessor(ABC):
    """A callable plugin that transforms raw document text.

    Implementations must raise ``TypeError`` for ``None`` or non-string input.
    They must return an empty string when given an empty string.
    """

    @abstractmethod
    def __call__(self, text: str) -> str:
        """Transform one document's text."""

    @abstractmethod
    def display_name(self) -> str:
        """Return the stable name used to display this plugin."""

    def __repr__(self) -> str:
        return self.display_name()


class CasingNormalizer(Preprocessor):
    """Normalize one document to lowercase."""

    def __call__(self, text: str) -> str:
        raise NotImplementedError()

    def display_name(self) -> str:
        return "case_normalizer"


class SpecialCharacterRemover(Preprocessor):
    """Replace non-alphabetic, non-whitespace characters with spaces."""

    def __call__(self, text: str) -> str:
        raise NotImplementedError()

    def display_name(self) -> str:
        return "special_character_remover"
