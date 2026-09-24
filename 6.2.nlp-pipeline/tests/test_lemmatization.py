import pytest

from textpipeline import Lemmatizer, Token


def test_lemmatize_tokens_forwards_the_part_of_speech():
    lemmatizer = Lemmatizer(pos="v")
    assert lemmatizer.pos == "v"
    assert lemmatizer.display_name() == "lemmatizer(pos=v)"
    assert repr(lemmatizer) == "lemmatizer(pos=v)"
    lemmatizer.ensure_wordnet()
    assert lemmatizer([Token("running"), Token("played")]) == [
        Token("run"),
        Token("play"),
    ]


@pytest.mark.parametrize("invalid_tokens", [None, "tokens"])
def test_lemmatizer_rejects_invalid_tokens(invalid_tokens):
    with pytest.raises(TypeError):
        Lemmatizer()(invalid_tokens)


def test_lemmatizer_returns_no_tokens_for_empty_input():
    assert Lemmatizer()([]) == []
