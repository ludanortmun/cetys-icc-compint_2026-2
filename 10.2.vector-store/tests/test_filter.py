from vector_store import Document, VectorStore


def test_all_tags_before_top_k_and_case_sensitivity(model):
    store = VectorStore(model)
    store.add([Document("east"), Document("east copy", {"a"}),
               Document("diagonal", {"a", "b"}), Document("north", {"a", "b", "c"}),
               Document("west", {"A", "b"})])
    tags = {"a", "b"}
    assert [d.text for d, _ in store.search("query", k=1, metadata=tags)] == ["diagonal"]
    assert [d.text for d, _ in store.search("query", k=10, metadata=tags)] == ["diagonal", "north"]
    assert tags == {"a", "b"}
    assert store.search("query", metadata={"missing"}) == []
    assert [d.text for d, _ in store.search("query", metadata={"A"})] == ["west"]
    for tags in (None, set()):
        assert len(store.search("query", k=10, metadata=tags)) == 5
