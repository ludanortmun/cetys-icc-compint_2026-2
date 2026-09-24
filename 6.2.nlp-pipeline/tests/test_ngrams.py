import pytest

from textpipeline import NGramGenerator, Token


def test_make_ngrams_returns_separator_joined_tokens():
    bigrams = NGramGenerator(2)
    assert bigrams.display_name() == "ngram_generator(n=2)"
    assert repr(bigrams) == "ngram_generator(n=2)"
    assert bigrams([Token("very"), Token("good"), Token("food")]) == [
        Token("very<sep>good"),
        Token("good<sep>food"),
    ]


def test_make_ngrams_rejects_non_positive_sizes():
    with pytest.raises(ValueError):
        NGramGenerator(0)([Token("token")])


@pytest.mark.parametrize("invalid_tokens", [None, "tokens"])
def test_ngram_generator_rejects_invalid_tokens(invalid_tokens):
    with pytest.raises(TypeError):
        NGramGenerator(2)(invalid_tokens)


def test_ngram_generator_returns_no_tokens_for_empty_input():
    assert NGramGenerator(2)([]) == []
