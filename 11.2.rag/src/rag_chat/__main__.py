"""Supplied terminal interface; not scored."""

import argparse
import sys
from pathlib import Path

from .config import create_client, load_config
from .pipeline import RAGPipeline, load_documents, split_documents


def main():
    parser = argparse.ArgumentParser(description="Chat with the top-level .txt files in a directory.")
    parser.add_argument("directory", type=Path, help="Directory containing .txt documents (not recursive).")
    parser.add_argument("--rerank", action="store_true", help="Enable the optional reranking implementation.")
    parser.add_argument("--expand-query", action="store_true", help="Enable optional query expansion.")
    args = parser.parse_args()

    try:
        config = load_config(rerank=args.rerank, query_expansion=args.expand_query)
        documents = load_documents(args.directory)
        chunks = split_documents(documents, config.chunk_size, config.chunk_overlap)
        # Heavy models are loaded only for the real application, never on import.
        from sentence_transformers import CrossEncoder, SentenceTransformer

        encoder = SentenceTransformer(config.embedding_model, device="cpu")
        reranker = CrossEncoder(config.rerank_model, device="cpu") if config.rerank else None
        pipeline = RAGPipeline(config, encoder, create_client(), reranker)
        pipeline.build_index(chunks)
    except NotImplementedError:
        parser.exit(1, "Complete the pipeline methods in src/rag_chat/pipeline.py first.\n")
    except Exception as error:
        parser.exit(1, f"Cannot start chat: {error}\n")

    print(f"Indexed {len(documents)} files and {len(chunks)} chunks from {args.directory}.")
    print("Use /clear to reset history, /quit to exit, or press Ctrl+C/EOF.")
    while True:
        try:
            question = input("> ").strip()
            if not question:
                continue
            if question == "/quit":
                return
            if question == "/clear":
                pipeline.clear()
                print("Conversation cleared; index retained.")
                continue
            reply = pipeline.ask(question)
            print(reply.answer)
            print("Retrieved sources:")
            if not reply.sources:
                print("  (none)")
            for result in reply.sources:
                metadata = result.document.metadata
                ranking = f", rerank={result.rerank_score:.4f}" if result.rerank_score is not None else ""
                print(f"  [{metadata['chunk_id']}] {metadata['source']} (cosine={result.score:.4f}{ranking})")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        except NotImplementedError:
            print("Complete the requested pipeline method or optional extension first.", file=sys.stderr)
        except Exception as error:
            print(f"Request failed: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
