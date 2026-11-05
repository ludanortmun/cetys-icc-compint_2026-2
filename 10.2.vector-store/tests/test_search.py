import math

import pytest

from vector_store import Document, VectorStore


def test_cosine_order_scores_and_top_k(model):
    store = VectorStore(model)
    store.add([Document(t) for t in ["west", "diagonal", "east", "north", "east copy"]])
    results = store.search("query", k=20)
    assert [d.text for d, _ in results] == ["east", "east copy", "diagonal", "north", "west"]
    assert [s for _, s in results] == pytest.approx([1., 1., .6, 0., -1.])
    assert [d.text for d, _ in store.search("query")] == ["east", "east copy", "diagonal"]
    assert len(store.search("query", k=1)) == 1


def test_zero_vectors_and_empty_store(model):
    store = VectorStore(model)
    assert store.search("query") == []
    store.add([Document("zero"), Document("east"), Document("west")])
    assert [s for _, s in store.search("zero")] == [0., 0., 0.]
    assert [d.text for d, _ in store.search("zero")] == ["zero", "east", "west"]
    scores = [s for _, s in store.search("query")]
    assert all(math.isfinite(s) for s in scores)
    assert scores == pytest.approx([1., 0., -1.])


def test_do_not_round_before_sorting(model):
    store = VectorStore(model)
    store.add([Document("almost east"), Document("east")])
    results = store.search("query")
    assert [d.text for d, _ in results] == ["east", "almost east"]
    assert results[0][1] > results[1][1]


@pytest.mark.parametrize("k", [0, -1])
def test_invalid_k_even_when_empty(model, k):
    store = VectorStore(model)
    with pytest.raises(ValueError):
        store.search("query", k=k)
    store.add([Document("east")])
    with pytest.raises(ValueError):
        store.search("query", k=k)
