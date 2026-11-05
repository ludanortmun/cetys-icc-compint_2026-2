import pytest

from vector_store import Document, VectorStore


def snapshot(store, **kwargs):
    return [(d.text, d.metadata, s) for d, s in store.search("query", k=20, **kwargs)]


def test_round_trip_explicit_paths_no_reencoding_and_append(model, tmp_path):
    store = VectorStore(model)
    store.add([Document("east", {"a", "tag with spaces"}), Document("east copy"),
               Document("unicode café 🐈", {"ñ"}), Document("zero")])
    expected = snapshot(store)
    path = tmp_path / "custom.store"
    store.save(path)
    assert path.is_file()
    model.calls.clear()
    loaded = VectorStore.load(str(path), model)
    assert model.calls == []
    assert snapshot(loaded) == expected
    assert snapshot(loaded, metadata={"a"}) == [expected[0]]
    loaded.add([Document("west")])
    assert len(snapshot(loaded)) == 5
    assert len(snapshot(store)) == 4
    other = tmp_path / "second.file"
    loaded.save(str(other))
    assert snapshot(VectorStore.load(other, model)) == snapshot(loaded)
    empty = VectorStore(model)
    empty.save(path)  # overwrite, including previously nonempty files
    restored = VectorStore.load(path, model)
    assert restored.search("query") == []
    restored.add([Document("north")])
    assert len(restored.search("query")) == 1


def test_missing_file(model, tmp_path):
    with pytest.raises(FileNotFoundError):
        VectorStore.load(tmp_path / "missing", model)
