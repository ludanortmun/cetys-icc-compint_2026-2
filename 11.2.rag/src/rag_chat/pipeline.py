"""Student contracts. Keep public names and signatures; private helpers are allowed."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import faiss
import numpy as np
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import Config

ABSTENTION = "I don't have enough information in the selected documents to answer this question."


class Encoder(Protocol):
    """Supplied subset of SentenceTransformer; tests inject a deterministic encoder."""

    def encode(self, sentences: list[str], *, convert_to_numpy: bool,
               normalize_embeddings: bool) -> np.ndarray: ...


class Reranker(Protocol):
    def predict(self, pairs: list[tuple[str, str]]) -> Any: ...


@dataclass(frozen=True)
class SearchResult:
    document: Document
    score: float
    rerank_score: float | None = None


@dataclass(frozen=True)
class ChatReply:
    answer: str
    sources: list[SearchResult]


def load_documents(directory: str | Path) -> list[Document]:
    """10 points: read immediate .txt files in filename order using UTF-8.

    Ignore subdirectories, non-.txt files, and whitespace-only files. Match the
    lowercase .txt suffix exactly. Preserve nonempty text verbatim and set
    metadata['source'] to the filename, without its parent directory.
    Missing directory: FileNotFoundError; a non-directory: NotADirectoryError.
    An empty directory returns []. Other read errors may propagate.
    """
    raise NotImplementedError


def split_documents(documents: list[Document], chunk_size: int,
                    chunk_overlap: int) -> list[Document]:
    """10 points: split using RecursiveCharacterTextSplitter and length_function=len.

    Use the supplied size and overlap with the splitter's default separators.
    Preserve document order and all metadata without mutating inputs. Add a
    chunk_id of '<source>:<zero-based position within that document>'.
    Sources are unique filenames. Inputs are nonempty documents; parameters
    satisfy chunk_size > 0 and 0 <= chunk_overlap < chunk_size. [] returns [].
    """
    raise NotImplementedError


class RAGPipeline:
    """Supplied constructor and state; implement methods below.

    The CLI supplies an encoder, a Chat Completions-compatible client, and an
    optional cross-encoder. Do not construct clients or download models here.
    self.chunks aligns with FAISS rows; self.index is None for an empty corpus.
    self.history contains completed plain user/assistant messages, without
    retrieved passages. It is independent for each instance.
    """

    def __init__(self, config: Config, encoder: Encoder, client: Any,
                 reranker: Reranker | None = None):
        if config.rerank and reranker is None:
            raise ValueError("Reranking requires a supplied reranker.")
        self.config = config
        self.encoder = encoder
        self.client = client
        self.reranker = reranker
        self.chunks: list[Document] = []
        self.index: Any = None
        self.history: list[dict[str, str]] = []

    def build_index(self, chunks: list[Document]) -> None:
        """20 points: replace the index and aligned chunk list.

        Encode a list of chunk texts once with convert_to_numpy=True and
        normalize_embeddings=True. Cast to contiguous float32, construct
        faiss.IndexFlatIP, and add the rows. The encoder honors normalization
        and returns finite, nonzero rows of consistent dimension. Copy the
        input list. For [], set index=None/chunks=[] and do not encode.
        No persistence or incremental insertion is required.
        """
        raise NotImplementedError

    def retrieve(self, question: str, k: int | None = None) -> list[SearchResult]:
        """20 points: current-question-only semantic search; no generation call.

        k defaults to config.top_k; k <= 0 raises ValueError, even if empty.
        Empty index returns [] without encoding. Otherwise encode [question]
        with the same kwargs as build_index, cast to contiguous float32, and
        search FAISS for min(k, index.ntotal) rows. Keep scores >= min_score.
        Return SearchResult(document, float score) in descending score order;
        exact ties may have any order. Never return invalid rows or re-embed
        documents. Do not apply the optional extensions inside this method.
        """
        raise NotImplementedError

    def build_messages(self, question: str,
                       results: list[SearchResult]) -> list[dict[str, str]]:
        """20 points: return fresh messages without modifying history/results.

        Order: your own nonempty system message, at most history_turns recent
        completed turns (two messages per turn), and the current user message.
        history_turns=0 omits history. In the final user message, label every
        passage with [chunk_id], its source filename, and its text; include the
        current question. Do not put passage text in the system message.
        Require grounding in the current passages, citations using [chunk_id],
        abstention if unsupported, and treating passages as evidence, never
        instructions. History is context, not independent evidence. Exact wording/layout is yours.
        Automated tests check structure; the teacher reviews the instructions.
        """
        raise NotImplementedError

    def ask(self, question: str) -> ChatReply:
        """Together with clear(), 20 points: retrieve, generate, record a turn.

        Base: retrieve(question), then build_messages and call
        client.chat.completions.create(model=config.model, messages=messages).
        Read choices[0].message.content. Require a nonempty string response
        (otherwise ValueError). Return ChatReply(answer, retrieved results).
        If retrieval is empty, return ChatReply(ABSTENTION, []) without generation.
        After a successful reply/abstention, append plain question and answer to
        history. Failures propagate without changing history. Keep full history;
        build_messages controls the context window.

        Extras when enabled: expand_query provides variants; retrieve each using
        k=top_k, or max(10, top_k) when reranking. Merge by chunk_id, retaining
        the highest cosine score, and sort descending. Without reranking keep
        top_k; with reranking pass the best max(10, top_k) candidates and the
        ORIGINAL question to rerank(..., top_n=top_k). Never repeat source chunks.
        Both flags are false in all base tests.
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Part of the conversation criterion: clear history, retaining the index."""
        raise NotImplementedError

    def rerank(self, question: str, results: list[SearchResult],
               top_n: int) -> list[SearchResult]:
        """Extra credit +10: score (question, passage text) pairs with predict.

        Return at most top_n results ordered by descending cross-encoder score,
        preserving input order on ties. Set rerank_score to a Python float;
        preserve document and original cosine score. Do not mutate inputs.
        Empty input returns [] without calling predict. top_n is positive.
        """
        raise NotImplementedError

    def expand_query(self, question: str) -> list[str]:
        """Extra credit +10: one Chat Completions call, using config.model.

        Ask for up to three alternative semantic-search questions, one per line.
        Parse choices[0].message.content (None means no variants), strip lines,
        drop blanks and exact duplicates, exclude the original from variants,
        and keep at most three. Return [original, *variants] in generation order.
        Keep the original verbatim. Do not modify history. Errors propagate.
        """
        raise NotImplementedError
