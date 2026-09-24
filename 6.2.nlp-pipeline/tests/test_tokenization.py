import pytest

from textpipeline import Token, WordTokenizer


def test_tokenize_words_returns_word_tokens_only():
    tokenizer = WordTokenizer()
    assert tokenizer.display_name() == "word_tokenizer"
    assert repr(tokenizer) == "word_tokenizer"
    assert tokenizer("very good-food!") == [Token("very"), Token("good"), Token("food")]


@pytest.mark.parametrize("invalid_text", [None, 42])
def test_word_tokenizer_rejects_invalid_text(invalid_text):
    with pytest.raises(TypeError):
        WordTokenizer()(invalid_text)


def test_word_tokenizer_returns_no_tokens_for_empty_text():
    assert WordTokenizer()("") == []
