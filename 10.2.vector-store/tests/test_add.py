from vector_store import Document, VectorStore


def test_append_alignment_duplicates_and_cached_embeddings(model):
    store = VectorStore(model)
    assert model.calls == []
    store.add([])
    assert model.calls == []
    store.add([Document("north", {"first"}), Document("east", {"second"})])
    store.add([Document("east", {"duplicate"})])
    assert [t for batch in model.calls for t in batch] == ["north", "east", "east"]
    before = len(model.calls)
    results = store.search("query", k=10)
    assert [(d.text, d.metadata) for d, _ in results] == [
        ("east", {"second"}), ("east", {"duplicate"}), ("north", {"first"})]
    assert model.calls[before:] == [["query"]]
    assert VectorStore(model).search("query") == []
