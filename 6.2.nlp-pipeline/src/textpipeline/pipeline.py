"""Orchestration for document-level text pipelines."""

from collections.abc import Iterable

from textpipeline.postprocessor import Postprocessor
from textpipeline.preprocessor import Preprocessor
from textpipeline.tokenizer import Token, Tokenizer, WordTokenizer


class TextPipeline:
    """Run typed processing phases for one document at a time."""

    def __init__(
        self,
        preprocessors: Iterable[Preprocessor] | None = None,
        tokenizer: Tokenizer | None = None,
        postprocessors: Iterable[Postprocessor] | None = None,
    ) -> None:
        self.preprocessors = list(preprocessors) if preprocessors is not None else []
        self.tokenizer = tokenizer if tokenizer is not None else WordTokenizer()
        self.postprocessors = list(postprocessors) if postprocessors is not None else []
        self.vocabulary: set[Token] = set()

    def __repr__(self) -> str:
        pre_names = ", ".join(repr(step) for step in self.preprocessors)
        post_names = ", ".join(repr(step) for step in self.postprocessors)
        return (
            "textpipeline: {steps: "
            f"{{pre: ({pre_names}), tokenizer: ({self.tokenizer!r}), "
            f"post: ({post_names})}}, vocab_size: {len(self.vocabulary)}}}"
        )

    def process(self, document: str, *, update_vocab: bool = False) -> list[Token]:
        """Process one document and optionally learn its final tokens.

        When ``update_vocab`` is false, tokens absent from the existing
        vocabulary are returned as ``Token("<unk>")`` instead.
        """
        raise NotImplementedError()
