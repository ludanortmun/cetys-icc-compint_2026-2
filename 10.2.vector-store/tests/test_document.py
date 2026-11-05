from vector_store import Document


def test_text_and_independent_optional_tags():
    tags = {"Topic", " arbitrary tag "}
    doc = Document("  café 🐈\n", tags)
    assert doc.text == "  café 🐈\n"
    assert doc.metadata == tags
    tags.add("later")
    assert "later" not in doc.metadata
    a, b, c = Document("a"), Document("b"), Document("c", None)
    assert a.metadata == b.metadata == c.metadata == set()
    a.metadata.add("only a")
    assert b.metadata == c.metadata == set()
