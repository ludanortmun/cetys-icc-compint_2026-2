"""Local RAG application. Import public types from rag.config and rag.pipeline.

Keep this initializer free of eager imports so rag.chat can load the model
runtime before rag.pipeline imports FAISS (required by the tested macOS wheels).
"""
