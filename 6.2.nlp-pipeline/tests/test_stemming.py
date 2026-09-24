import pytest

from textpipeline import SimpleStemmer, Token


def test_stem_tokens_removes_the_taught_suffixes():
    tokens = [Token("playing"), Token("baked"), Token("cats"), Token("king")]
    stemmer = SimpleStemmer()
    assert stemmer.display_name() == "simple_stemmer"
    assert repr(stemmer) == "simple_stemmer"
    assert stemmer(tokens) == [Token("play"), Token("bak"), Token("cat"), Token("king")]


@pytest.mark.parametrize("invalid_tokens", [None, "tokens"])
def test_simple_stemmer_rejects_invalid_tokens(invalid_tokens):
    with pytest.raises(TypeError):
        SimpleStemmer()(invalid_tokens)


def test_simple_stemmer_returns_no_tokens_for_empty_input():
    assert SimpleStemmer()([]) == []
